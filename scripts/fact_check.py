"""Fact-checker for evaluation results.

Loads a results JSON file, sends each response to the Grok API with a
fact-check prompt, and outputs a structured report.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, APIError, APIConnectionError, RateLimitError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FACT_CHECK_MODEL = "grok-3-mini"
RATE_LIMIT_DELAY = 2.0
MAX_RETRIES = 2
RETRY_BACKOFF = 3.0

FACT_CHECK_SYSTEM = """You are a fact-checker. Given an AI model's response to a prompt, do the following:

1. Extract the 3-5 most important factual claims from the response.
2. For each claim, assess whether it is: VERIFIED (likely true), UNVERIFIED (cannot confirm), or FALSE (likely wrong).
3. Provide a confidence level (high/medium/low) for your assessment.
4. Give a brief explanation for each verdict.

Respond in this exact JSON format (no markdown, just raw JSON):
{
  "claims": [
    {
      "claim": "the factual claim extracted",
      "verdict": "VERIFIED|UNVERIFIED|FALSE",
      "confidence": "high|medium|low",
      "explanation": "why you reached this verdict"
    }
  ],
  "overall_reliability": "high|medium|low",
  "summary": "one sentence overall assessment"
}"""


def load_results(path: str) -> dict:
    """Load a results JSON file."""
    results_path = Path(path)
    if not results_path.exists():
        print(f"Error: file not found: {results_path}")
        sys.exit(1)

    with open(results_path) as f:
        return json.load(f)


def fact_check_response(
    client: OpenAI,
    prompt_text: str,
    response_text: str,
) -> dict:
    """Send a fact-check request for one response."""
    user_msg = (
        f"ORIGINAL PROMPT:\n{prompt_text}\n\nAI RESPONSE TO CHECK:\n{response_text}"
    )

    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=FACT_CHECK_MODEL,
                messages=[
                    {"role": "system", "content": FACT_CHECK_SYSTEM},
                    {"role": "user", "content": user_msg},
                ],
            )
            raw = response.choices[0].message.content or ""
            # Try to parse as JSON, fall back to raw text
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                # Strip markdown fences if present
                cleaned = raw.strip()
                if cleaned.startswith("```"):
                    lines = cleaned.split("\n")
                    lines = [
                        line for line in lines if not line.strip().startswith("```")
                    ]
                    cleaned = "\n".join(lines)
                try:
                    return json.loads(cleaned)
                except json.JSONDecodeError:
                    return {
                        "claims": [],
                        "overall_reliability": "unknown",
                        "summary": f"Could not parse fact-check response. Raw: {raw[:500]}",
                    }

        except (APIError, APIConnectionError, RateLimitError) as exc:
            last_error = exc
            print(f"  Attempt {attempt}/{MAX_RETRIES} failed: {exc}")
            if attempt < MAX_RETRIES:
                backoff = RETRY_BACKOFF * attempt
                time.sleep(backoff)

    return {
        "claims": [],
        "overall_reliability": "error",
        "summary": f"API error: {last_error}",
    }


def run_fact_check(results_path: str) -> dict:
    """Run fact-checking on all responses in a results file."""
    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("GROK_API_KEY")
    if not api_key:
        print("Error: GROK_API_KEY not set in .env")
        sys.exit(1)

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
    )

    data = load_results(results_path)
    results = data.get("results", [])
    print(f"Fact-checking {len(results)} responses from: {results_path}")
    print(f"Using model: {FACT_CHECK_MODEL}")
    print()

    report = {
        "metadata": {
            "source_file": results_path,
            "source_area": data.get("metadata", {}).get("area", "unknown"),
            "source_model": data.get("metadata", {}).get("model", "unknown"),
            "fact_check_model": FACT_CHECK_MODEL,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "checks": [],
    }

    for entry in results:
        idx = entry.get("index", "?")
        fname = entry.get("file", "unknown")
        print(f"[{idx}] {fname}")

        # Support both old schema (response_text) and new challenge schema (phase1_response)
        response_text = entry.get("response_text") or entry.get("phase1_response")
        phase2 = entry.get("phase2_response")
        if phase2:
            response_text = f"{response_text}\n\n[Challenge Response]:\n{phase2}"
        if not response_text:
            print("  SKIP: no response text")
            report["checks"].append(
                {
                    "index": idx,
                    "file": fname,
                    "skipped": True,
                    "reason": "no response text",
                }
            )
            continue

        prompt_text = entry.get("prompt_text", "")
        check = fact_check_response(client, prompt_text, response_text)

        claim_count = len(check.get("claims", []))
        reliability = check.get("overall_reliability", "?")
        print(f"  {claim_count} claims checked | reliability: {reliability}")

        report["checks"].append(
            {
                "index": idx,
                "file": fname,
                "skipped": False,
                **check,
            }
        )

        time.sleep(RATE_LIMIT_DELAY)

    # Save report
    source = Path(results_path)
    out_name = f"factcheck_{source.stem}.json"
    out_file = source.parent / out_name

    with open(out_file, "w") as f:
        json.dump(report, f, indent=2)

    print()
    print(f"Fact-check report saved to: {out_file}")

    # Summary
    checked = [c for c in report["checks"] if not c.get("skipped")]
    total_claims = sum(len(c.get("claims", [])) for c in checked)
    verdicts = {}
    for c in checked:
        for claim in c.get("claims", []):
            v = claim.get("verdict", "UNKNOWN")
            verdicts[v] = verdicts.get(v, 0) + 1

    print(f"Total claims extracted: {total_claims}")
    for verdict, count in sorted(verdicts.items()):
        print(f"  {verdict}: {count}")

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Fact-check evaluation results")
    parser.add_argument(
        "--run",
        required=True,
        help="Path to a results JSON file from run_eval.py",
    )
    args = parser.parse_args()

    run_fact_check(args.run)


if __name__ == "__main__":
    main()
