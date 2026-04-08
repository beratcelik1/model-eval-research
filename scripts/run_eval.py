"""Evaluation runner for Grok with integrated challenge-response.

Each prompt runs in its own conversation. When challenge mode is enabled,
Phase 2 stays in the same prompt-level conversation so the model can revise
its own answer without leaking answer-key context into later prompts.
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
from eval_schema import AnswerKeyPrompt, parse_answer_key

# Grok's API is OpenAI-compatible, so we use the openai SDK
# pointed at api.x.ai instead of api.openai.com.
from openai import OpenAI, APIError, APIConnectionError, RateLimitError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
AREAS = ["investment-decisions", "marketing-behavior", "health-longevity"]
MODELS = {
    "validate": "grok-4-1-fast-reasoning",
    "final": "grok-4.20-0309-reasoning",
}
RATE_LIMIT_DELAY = 2.0
CHALLENGE_THRESHOLD = 70.0  # Only challenge if Phase 1 scores below this %
MAX_RETRIES = 2
RETRY_BACKOFF = 3.0


def extract_prompt_only(text: str) -> str:
    """Extract only the prompt text, stripping scoring metadata."""
    parts = text.strip().split("\n---")
    prompt_text = parts[0].strip()
    if not prompt_text:
        print("  WARNING: Empty prompt text, sending full file")
        return text.strip()
    return prompt_text


def load_prompts(area: str) -> list[dict[str, str]]:
    """Load prompt .md files from areas/{area}/prompts/."""
    prompts_dir = PROJECT_ROOT / "areas" / area / "prompts"
    if not prompts_dir.exists():
        print(f"Error: prompts directory not found: {prompts_dir}")
        sys.exit(1)

    prompt_files = sorted(prompts_dir.glob("*.md"))
    if not prompt_files:
        print(f"Error: no .md files in {prompts_dir}")
        sys.exit(1)

    prompts = []
    for pf in prompt_files:
        full_text = pf.read_text().strip()
        prompt_text = extract_prompt_only(full_text)
        prompts.append(
            {
                "file": pf.name,
                "full_text": full_text,
                "text": prompt_text,
            }
        )
    return prompts


def load_answer_key(area: str) -> dict[int, AnswerKeyPrompt]:
    """Load and parse an area's answer key."""
    key_path = PROJECT_ROOT / "areas" / area / "answer-key.md"
    if not key_path.exists():
        return {}

    return parse_answer_key(key_path)


def build_challenge(answer_key_entry: AnswerKeyPrompt) -> str | None:
    """Build a challenge follow-up from answer key data.

    Prefer the authored challenge when one exists. Otherwise synthesize a
    challenge from the answer-key evidence sections.
    """
    authored = answer_key_entry.first_challenge_text()
    if authored:
        return authored

    evidence_sections = answer_key_entry.evidence_sections()
    if not evidence_sections:
        return None

    evidence_chunks = []
    for section in evidence_sections:
        if not section.body:
            continue
        evidence_chunks.append(f"{section.title}\n{section.body}")
        if len(evidence_chunks) >= 3:
            break

    if not evidence_chunks:
        return None

    return (
        "I want to pressure-test your earlier answer against the research notes below. "
        "Please do not agree automatically. Keep what is well supported, reject what is weak, "
        "and give me a revised answer that is more accurate than both your first answer and my notes.\n\n"
        + "\n\n".join(evidence_chunks)
    )


def send_messages(
    client: OpenAI,
    model: str,
    messages: list[dict[str, str]],
) -> dict:
    """Send a conversation to the Grok API with retry logic."""
    last_error: Exception | None = None

    for attempt in range(1, MAX_RETRIES + 1):
        start = time.monotonic()
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=4096,
                temperature=0,
                timeout=120,
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

    # No automated classification - responses are too nuanced for string matching.
    # Use grade_responses.py for checklist-based scoring after the run.


def run_eval(
    area: str,
    mode: str,
    challenge: bool = False,
    dry_run: bool = False,
) -> dict:
    """Run the full evaluation pipeline for one area.

    If challenge=True and an answer key exists, sends a follow-up challenge
    in the SAME conversation context after each initial response.
    """
    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("GROK_API_KEY")
    if not api_key and not dry_run:
        print("Error: GROK_API_KEY not set in .env")
        sys.exit(1)

    model = MODELS[mode]
    prompts = load_prompts(area)
    answer_key = load_answer_key(area) if challenge else {}

    print(f"Loaded {len(prompts)} prompts for area: {area}")
    print(
        f"Mode: {mode} | Model: {model} | Challenge: {challenge} | Dry run: {dry_run}"
    )
    if answer_key:
        print(f"Answer key loaded: {len(answer_key)} entries")
    print()

    ts = datetime.now(timezone.utc)
    ts_str = ts.strftime("%Y%m%d_%H%M%S")

    results = {
        "metadata": {
            "area": area,
            "mode": mode,
            "model": model,
            "challenge_enabled": challenge,
            "timestamp": ts.isoformat(),
            "dry_run": dry_run,
            "prompt_count": len(prompts),
        },
        "results": [],
    }

    client: OpenAI | None = None
    if not dry_run:
        client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

    for i, prompt in enumerate(prompts, 1):
        print(f"[{i}/{len(prompts)}] {prompt['file']}")

        # === PHASE 1: Initial prompt ===
        if dry_run:
            preview = prompt["text"][:200]
            print(f"  PHASE 1 PREVIEW: {preview}...")
            entry = {
                "index": i,
                "file": prompt["file"],
                "prompt_text": prompt["text"],
                "phase1_response": None,
                "phase1_tokens": None,
                "phase1_time_s": None,
                "challenge_sent": False,
                "challenge_text": None,
                "phase2_response": None,
                "phase2_tokens": None,
                "phase2_time_s": None,
                "outcome": "DRY_RUN",
                "error": None,
            }

            # Show challenge preview if available
            if i in answer_key:
                challenge_text = build_challenge(answer_key[i])
                if challenge_text:
                    entry["challenge_text"] = challenge_text[:300]
                    print(f"  PHASE 2 PREVIEW: {challenge_text[:200]}...")

            results["results"].append(entry)
            print()
            continue

        assert client is not None
        messages = [{"role": "user", "content": prompt["text"]}]
        phase1 = send_messages(client, model, messages)

        if phase1["error"]:
            print(f"  PHASE 1 ERROR: {phase1['error']}")
            results["results"].append(
                {
                    "index": i,
                    "file": prompt["file"],
                    "prompt_text": prompt["text"],
                    "phase1_response": None,
                    "phase1_tokens": None,
                    "phase1_time_s": None,
                    "challenge_sent": False,
                    "challenge_text": None,
                    "phase2_response": None,
                    "phase2_tokens": None,
                    "phase2_time_s": None,
                    "outcome": "ERROR",
                    "error": phase1["error"],
                }
            )
            time.sleep(RATE_LIMIT_DELAY)
            continue

        phase1_text = phase1["response_text"] or ""
        print(
            f"  PHASE 1: {phase1['total_tokens']} tokens | {phase1['response_time_s']}s"
        )

        # === INLINE GRADING of Phase 1 ===
        phase1_score = 0.0
        phase1_checklist: list[dict] = []
        if challenge and i in answer_key:
            from grade_responses import (
                auto_check_item,
                extract_checklist_items,
                weighted_percentage,
                weighted_present,
                weighted_total,
            )

            phase1_checklist = extract_checklist_items(answer_key[i])
            if phase1_checklist:
                for item in phase1_checklist:
                    item["present_phase1"] = auto_check_item(item, phase1_text)
                present = sum(
                    1 for it in phase1_checklist if it["present_phase1"] is True
                )
                phase1_score = weighted_percentage(
                    weighted_present(phase1_checklist, "present_phase1"),
                    weighted_total(phase1_checklist),
                )
                print(
                    f"  GRADE: {present}/{len(phase1_checklist)} items "
                    f"({phase1_score:.0f}% weighted)"
                )

        entry = {
            "index": i,
            "file": prompt["file"],
            "prompt_text": prompt["text"],
            "phase1_response": phase1_text,
            "phase1_tokens": phase1["total_tokens"],
            "phase1_time_s": phase1["response_time_s"],
            "phase1_score_pct": round(phase1_score, 1),
            "phase1_items_present": sum(
                1 for it in phase1_checklist if it["present_phase1"] is True
            ),
            "phase1_items_total": len(phase1_checklist),
            "challenge_sent": False,
            "challenge_text": None,
            "phase2_response": None,
            "phase2_tokens": None,
            "phase2_time_s": None,
            "outcome": (
                "PASS"
                if phase1_score >= CHALLENGE_THRESHOLD
                else "CHALLENGE_ELIGIBLE"
            ),
            "error": None,
        }

        # === PHASE 2: Only challenge if Phase 1 score is below threshold ===
        if challenge and i in answer_key and phase1_score < CHALLENGE_THRESHOLD:
            challenge_text = build_challenge(answer_key[i])

            if challenge_text:
                print(
                    f"  Phase 1 below {CHALLENGE_THRESHOLD:.0f}% threshold, sending challenge..."
                )
                time.sleep(RATE_LIMIT_DELAY)

                # Build multi-turn conversation so Grok has full context
                messages = [
                    {"role": "user", "content": prompt["text"]},
                    {"role": "assistant", "content": phase1_text},
                    {"role": "user", "content": challenge_text},
                ]

                phase2 = send_messages(client, model, messages)
                entry["challenge_sent"] = True
                entry["challenge_text"] = challenge_text

                if phase2["error"]:
                    print(f"  PHASE 2 ERROR: {phase2['error']}")
                    entry["error"] = phase2["error"]
                else:
                    phase2_text = phase2["response_text"] or ""
                    entry["phase2_response"] = phase2_text
                    entry["phase2_tokens"] = phase2["total_tokens"]
                    entry["phase2_time_s"] = phase2["response_time_s"]
                    entry["outcome"] = "CHALLENGED"
                    print(
                        f"  PHASE 2: {phase2['total_tokens']} tokens | {phase2['response_time_s']}s"
                    )
        elif challenge and phase1_score >= CHALLENGE_THRESHOLD:
            print(
                f"  Phase 1 above {CHALLENGE_THRESHOLD:.0f}% threshold, PASS - skipping challenge"
            )

        results["results"].append(entry)

        if i < len(prompts):
            time.sleep(RATE_LIMIT_DELAY)

    # Save results
    suffix = "_challenge" if challenge else ""
    out_dir = PROJECT_ROOT / "experiments" / mode
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{area}{suffix}_{ts_str}.json"

    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)

    print()
    print(f"Results saved to: {out_file}")

    # Summary
    outcomes = [r["outcome"] for r in results["results"]]
    print("\nSummary:")
    for outcome in [
        "PASS",
        "CHALLENGE_ELIGIBLE",
        "CHALLENGED",
        "ERROR",
        "DRY_RUN",
    ]:
        count = outcomes.count(outcome)
        if count > 0:
            print(f"  {outcome}: {count}")

    total_tokens = sum(
        (r.get("phase1_tokens") or 0) + (r.get("phase2_tokens") or 0)
        for r in results["results"]
    )
    print(f"  Total tokens used: {total_tokens}")

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Grok evaluation")
    parser.add_argument(
        "--mode",
        choices=["validate", "final"],
        required=True,
        help="validate = grok-4-1-fast-reasoning, final = grok-4.20-0309-reasoning",
    )
    parser.add_argument(
        "--area",
        choices=AREAS,
        required=True,
    )
    parser.add_argument(
        "--challenge",
        action="store_true",
        help="Enable Phase 2 challenge-response using answer keys",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview prompts without API calls",
    )
    args = parser.parse_args()

    run_eval(
        area=args.area,
        mode=args.mode,
        challenge=args.challenge,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
