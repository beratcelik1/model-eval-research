"""Evaluation runner for Grok API model testing.

Loads prompts from areas/{area}/prompts/*.md, sends them to the Grok API,
and records structured results to experiments/{mode}/.
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
AREAS = ["investment-decisions", "marketing-behavior", "health-longevity"]
MODELS = {
    "validate": "grok-3-mini",
    "final": "grok-3",
}
RATE_LIMIT_DELAY = 2.0
MAX_RETRIES = 2
RETRY_BACKOFF = 3.0


def load_prompts(area: str) -> list[dict[str, str]]:
    """Load all prompt .md files from areas/{area}/prompts/, sorted by name."""
    prompts_dir = PROJECT_ROOT / "areas" / area / "prompts"
    if not prompts_dir.exists():
        print(f"Error: prompts directory not found: {prompts_dir}")
        sys.exit(1)

    prompt_files = sorted(prompts_dir.glob("*.md"))
    if not prompt_files:
        print(f"Error: no .md files found in {prompts_dir}")
        print("Run extract_prompts.py first to generate prompt files.")
        sys.exit(1)

    prompts = []
    for pf in prompt_files:
        text = pf.read_text().strip()
        prompts.append(
            {
                "file": pf.name,
                "text": text,
            }
        )
    return prompts


def send_prompt(
    client: OpenAI,
    model: str,
    prompt_text: str,
) -> dict:
    """Send a single prompt to the Grok API with retry logic.

    Returns a dict with response text, token counts, and timing.
    """
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
            elapsed = time.monotonic() - start
            print(f"  Attempt {attempt}/{MAX_RETRIES} failed: {exc}")
            if attempt < MAX_RETRIES:
                backoff = RETRY_BACKOFF * attempt
                print(f"  Retrying in {backoff}s...")
                time.sleep(backoff)

    return {
        "response_text": None,
        "finish_reason": "error",
        "prompt_tokens": None,
        "completion_tokens": None,
        "total_tokens": None,
        "response_time_s": None,
        "error": str(last_error),
    }


def run_eval(
    area: str,
    mode: str,
    dry_run: bool = False,
) -> dict:
    """Run the full evaluation pipeline for one area."""
    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("GROK_API_KEY")
    if not api_key and not dry_run:
        print("Error: GROK_API_KEY not set in .env")
        sys.exit(1)

    model = MODELS[mode]
    prompts = load_prompts(area)
    print(f"Loaded {len(prompts)} prompts for area: {area}")
    print(f"Mode: {mode} | Model: {model} | Dry run: {dry_run}")
    print()

    ts = datetime.now(timezone.utc)
    ts_str = ts.strftime("%Y%m%d_%H%M%S")

    results = {
        "metadata": {
            "area": area,
            "mode": mode,
            "model": model,
            "timestamp": ts.isoformat(),
            "dry_run": dry_run,
            "prompt_count": len(prompts),
        },
        "results": [],
    }

    client: OpenAI | None = None
    if not dry_run:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1",
        )

    for i, prompt in enumerate(prompts, 1):
        print(f"[{i}/{len(prompts)}] {prompt['file']}")

        if dry_run:
            preview = prompt["text"][:200]
            print(f"  PREVIEW: {preview}...")
            print()
            results["results"].append(
                {
                    "index": i,
                    "file": prompt["file"],
                    "prompt_text": prompt["text"],
                    "response_text": None,
                    "model": model,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "prompt_tokens": None,
                    "completion_tokens": None,
                    "total_tokens": None,
                    "response_time_s": None,
                    "finish_reason": "dry_run",
                    "error": None,
                }
            )
            continue

        assert client is not None
        api_result = send_prompt(client, model, prompt["text"])

        entry = {
            "index": i,
            "file": prompt["file"],
            "prompt_text": prompt["text"],
            "response_text": api_result["response_text"],
            "model": model,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "prompt_tokens": api_result["prompt_tokens"],
            "completion_tokens": api_result["completion_tokens"],
            "total_tokens": api_result["total_tokens"],
            "response_time_s": api_result["response_time_s"],
            "finish_reason": api_result["finish_reason"],
            "error": api_result["error"],
        }
        results["results"].append(entry)

        status = (
            "OK" if api_result["error"] is None else f"ERROR: {api_result['error']}"
        )
        tokens = api_result["total_tokens"] or "?"
        elapsed = api_result["response_time_s"] or "?"
        print(f"  {status} | {tokens} tokens | {elapsed}s")

        if i < len(prompts):
            time.sleep(RATE_LIMIT_DELAY)

    # Save results
    out_dir = PROJECT_ROOT / "experiments" / mode
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{area}_{ts_str}.json"

    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)

    print()
    print(f"Results saved to: {out_file}")

    # Summary
    ok_count = sum(1 for r in results["results"] if r["error"] is None)
    err_count = sum(1 for r in results["results"] if r["error"] is not None)
    total_tokens = sum(r["total_tokens"] or 0 for r in results["results"])
    print(f"Summary: {ok_count} ok, {err_count} errors, {total_tokens} total tokens")

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Grok API evaluation")
    parser.add_argument(
        "--mode",
        choices=["validate", "final"],
        required=True,
        help="validate = grok-3-mini, final = grok-3",
    )
    parser.add_argument(
        "--area",
        choices=AREAS,
        required=True,
        help="Evaluation area",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview prompts without making API calls",
    )
    args = parser.parse_args()

    run_eval(area=args.area, mode=args.mode, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
