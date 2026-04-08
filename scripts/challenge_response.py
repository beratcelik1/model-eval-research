"""Challenge-response evaluation for Grok.

After an initial eval run, this script compares Grok's responses against
our answer key. For any gaps or errors found, it sends a follow-up challenge
with our evidence and sources, then records whether Grok:

1. PASS - Initial answer aligned with our research
2. FAIL-ACCEPTED - Grok missed something, accepted correction when shown evidence
3. FAIL-CONTESTED - Grok pushed back with counter-evidence (our proof may be incomplete)

Outcome 3 is the most valuable - it reveals either model stubbornness
OR genuine gaps in our own research.
"""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

# Grok's API is OpenAI-compatible
from openai import OpenAI, APIError, APIConnectionError, RateLimitError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RATE_LIMIT_DELAY = 3.0
MAX_RETRIES = 2
RETRY_BACKOFF = 3.0


def load_answer_key(area: str) -> dict[str, dict]:
    """Load the answer key for an area.

    Answer keys are markdown files with structured sections per prompt.
    Returns a dict keyed by prompt filename.
    """
    key_path = PROJECT_ROOT / "areas" / area / "answer-key.md"
    if not key_path.exists():
        print(f"Error: answer key not found: {key_path}")
        sys.exit(1)

    text = key_path.read_text()
    prompts: dict[str, dict] = {}
    current_prompt = None
    current_section = None
    current_lines: list[str] = []

    for line in text.split("\n"):
        stripped = line.strip()

        # New prompt section
        if stripped.startswith("### Prompt"):
            if current_prompt and current_section:
                prompts.setdefault(current_prompt, {})[current_section] = "\n".join(
                    current_lines
                ).strip()
            current_lines = []
            # Extract prompt number/name
            current_prompt = stripped.replace("### ", "").strip()
            current_section = None
            continue

        # Sub-sections within a prompt
        if stripped.startswith("**") and stripped.endswith("**"):
            if current_prompt and current_section:
                prompts.setdefault(current_prompt, {})[current_section] = "\n".join(
                    current_lines
                ).strip()
            current_section = stripped.strip("*").strip()
            current_lines = []
            continue

        if current_section:
            current_lines.append(line)

    # Save last section
    if current_prompt and current_section:
        prompts.setdefault(current_prompt, {})[current_section] = "\n".join(
            current_lines
        ).strip()

    return prompts


def load_eval_results(results_path: str) -> dict:
    """Load results from a previous eval run."""
    with open(results_path) as f:
        return json.load(f)


def build_challenge_prompt(
    original_prompt: str,
    grok_response: str,
    answer_key_section: dict,
) -> str | None:
    """Build a challenge prompt based on what Grok missed.

    Returns None if no challenge is needed (response looks adequate).
    """
    verified = answer_key_section.get("Verified correct benchmarks", "")
    debatable = answer_key_section.get(
        "Debatable points (multiple valid positions)", ""
    )

    if not verified and not debatable:
        return None

    challenge = (
        "I asked you the following question:\n\n"
        f"> {original_prompt}\n\n"
        "Your response was:\n\n"
        f"> {grok_response[:2000]}\n\n"
        "I'd like to challenge some aspects of your answer based on my research. "
        "Here is what I found:\n\n"
    )

    if verified:
        challenge += f"**Verified findings from research:**\n{verified}\n\n"

    if debatable:
        challenge += f"**Points where experts disagree:**\n{debatable}\n\n"

    challenge += (
        "Based on this evidence:\n"
        "1. What did your original response get right?\n"
        "2. What did your original response miss or get wrong?\n"
        "3. If you disagree with any of my research, explain why with specific sources.\n"
        "4. Give me a revised answer incorporating this feedback."
    )

    return challenge


def send_prompt(client: OpenAI, model: str, prompt_text: str) -> dict:
    """Send a prompt to the Grok API with retry logic."""
    last_error: Exception | None = None

    for attempt in range(1, MAX_RETRIES + 1):
        start = time.monotonic()
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt_text}],
            )
            elapsed = time.monotonic() - start
            choice = response.choices[0]
            usage = response.usage

            return {
                "response_text": choice.message.content,
                "finish_reason": choice.finish_reason,
                "prompt_tokens": usage.prompt_tokens if usage else None,
                "completion_tokens": usage.completion_tokens if usage else None,
                "total_tokens": usage.total_tokens if usage else None,
                "response_time_s": round(elapsed, 2),
                "error": None,
            }
        except (APIError, APIConnectionError, RateLimitError) as exc:
            last_error = exc
            print(f"  Attempt {attempt}/{MAX_RETRIES} failed: {exc}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * attempt)

    return {
        "response_text": None,
        "finish_reason": "error",
        "prompt_tokens": None,
        "completion_tokens": None,
        "total_tokens": None,
        "response_time_s": None,
        "error": str(last_error),
    }


def classify_challenge_response(challenge_response: str) -> str:
    """Classify Grok's response to the challenge.

    Returns one of:
    - FAIL-ACCEPTED: Grok acknowledged errors and revised
    - FAIL-CONTESTED: Grok pushed back with counter-evidence
    - UNCLEAR: Can't determine automatically
    """
    lower = challenge_response.lower()

    # Look for signs of acceptance
    accept_signals = [
        "you're right",
        "i should have",
        "i missed",
        "my original response",
        "i apologize",
        "that's a valid point",
        "i overlooked",
        "i failed to mention",
        "my response was incomplete",
        "i agree",
    ]

    # Look for signs of contestation
    contest_signals = [
        "i disagree",
        "however, my original",
        "i stand by",
        "your source may be",
        "there is conflicting evidence",
        "more recent research suggests",
        "actually,",
        "that interpretation is debatable",
        "the evidence is mixed",
        "i would push back",
    ]

    accept_count = sum(1 for s in accept_signals if s in lower)
    contest_count = sum(1 for s in contest_signals if s in lower)

    if contest_count >= 2:
        return "FAIL-CONTESTED"
    if accept_count >= 2:
        return "FAIL-ACCEPTED"
    if contest_count > accept_count:
        return "FAIL-CONTESTED"
    if accept_count > contest_count:
        return "FAIL-ACCEPTED"
    return "UNCLEAR"


def run_challenge_response(
    results_path: str,
    area: str,
    model: str = "grok-3",
    dry_run: bool = False,
) -> dict:
    """Run the challenge-response protocol against previous eval results."""
    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("GROK_API_KEY")
    if not api_key and not dry_run:
        print("Error: GROK_API_KEY not set in .env")
        sys.exit(1)

    eval_results = load_eval_results(results_path)
    answer_key = load_answer_key(area)

    print(f"Challenge-response for: {area}")
    print(f"Model: {model} | Dry run: {dry_run}")
    print(f"Answer key has {len(answer_key)} prompt entries")
    print()

    ts = datetime.now(timezone.utc)
    ts_str = ts.strftime("%Y%m%d_%H%M%S")

    challenge_results = {
        "metadata": {
            "area": area,
            "model": model,
            "source_eval": results_path,
            "timestamp": ts.isoformat(),
            "dry_run": dry_run,
        },
        "results": [],
    }

    client: OpenAI | None = None
    if not dry_run:
        client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

    for result in eval_results.get("results", []):
        prompt_file = result.get("file", "")
        original_prompt = result.get("prompt_text", "")
        grok_response = result.get("response_text", "")

        if not grok_response:
            continue

        # Find matching answer key entry
        matching_key = None
        for key_name, key_data in answer_key.items():
            # Match by prompt number
            prompt_num = result.get("index", 0)
            if f"Prompt {prompt_num}" in key_name:
                matching_key = key_data
                break

        if not matching_key:
            print(f"  [{prompt_file}] No answer key match - skipping")
            continue

        # Build challenge
        challenge_prompt = build_challenge_prompt(
            original_prompt, grok_response, matching_key
        )

        if not challenge_prompt:
            print(f"  [{prompt_file}] No challenge needed - PASS")
            challenge_results["results"].append(
                {
                    "file": prompt_file,
                    "outcome": "PASS",
                    "challenge_sent": False,
                    "challenge_response": None,
                }
            )
            continue

        print(f"  [{prompt_file}] Sending challenge...")

        if dry_run:
            print(f"    PREVIEW: {challenge_prompt[:200]}...")
            challenge_results["results"].append(
                {
                    "file": prompt_file,
                    "outcome": "DRY_RUN",
                    "challenge_sent": True,
                    "challenge_prompt": challenge_prompt[:500],
                    "challenge_response": None,
                }
            )
            continue

        assert client is not None
        api_result = send_prompt(client, model, challenge_prompt)

        if api_result["error"]:
            outcome = "ERROR"
        else:
            outcome = classify_challenge_response(api_result["response_text"] or "")

        challenge_results["results"].append(
            {
                "file": prompt_file,
                "outcome": outcome,
                "challenge_sent": True,
                "challenge_prompt": challenge_prompt,
                "challenge_response": api_result["response_text"],
                "tokens": api_result["total_tokens"],
                "response_time_s": api_result["response_time_s"],
            }
        )

        print(f"    Outcome: {outcome}")
        time.sleep(RATE_LIMIT_DELAY)

    # Save results
    out_dir = PROJECT_ROOT / "experiments" / "challenges"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{area}_{ts_str}.json"

    with open(out_file, "w") as f:
        json.dump(challenge_results, f, indent=2)

    # Summary
    outcomes = [r["outcome"] for r in challenge_results["results"]]
    print()
    print(f"Results saved to: {out_file}")
    print(f"PASS: {outcomes.count('PASS')}")
    print(f"FAIL-ACCEPTED: {outcomes.count('FAIL-ACCEPTED')}")
    print(f"FAIL-CONTESTED: {outcomes.count('FAIL-CONTESTED')}")
    print(f"UNCLEAR: {outcomes.count('UNCLEAR')}")

    return challenge_results


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Challenge-response evaluation against answer keys"
    )
    parser.add_argument(
        "--results",
        required=True,
        help="Path to eval results JSON from run_eval.py",
    )
    parser.add_argument(
        "--area",
        choices=["investment-decisions", "marketing-behavior", "health-longevity"],
        required=True,
    )
    parser.add_argument(
        "--model",
        default="grok-3",
        help="Model for challenge phase (default: grok-3)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview challenges without making API calls",
    )
    args = parser.parse_args()

    run_challenge_response(
        results_path=args.results,
        area=args.area,
        model=args.model,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
