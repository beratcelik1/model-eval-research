"""Structured checklist scoring for challenge routing.

The local grader is deliberately conservative. Its main job is to provide a
stable, reproducible gate for the challenge-response workflow and to surface
items that still need closer review.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from eval_schema import (
    AnswerKeyPrompt,
    CHECKLIST_SECTION_KINDS,
    extract_keywords,
    iter_checklist_lines,
    parse_answer_key,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_answer_key(area: str) -> dict[int, AnswerKeyPrompt]:
    """Load and parse an area's answer key."""
    key_path = PROJECT_ROOT / "areas" / area / "answer-key.md"
    if not key_path.exists():
        print(f"Error: answer key not found: {key_path}")
        sys.exit(1)
    return parse_answer_key(key_path)


def extract_checklist_items(answer_key_entry: AnswerKeyPrompt) -> list[dict]:
    """Convert a parsed answer-key prompt into checklist items."""
    items: list[dict] = []

    for section in answer_key_entry.sections:
        if section.kind not in CHECKLIST_SECTION_KINDS:
            continue

        for line in iter_checklist_lines(section):
            if len(line) < 10:
                continue

            number_keywords = re.findall(r"[-+]?\$?[\d,]+\.?\d*", line)
            item_type = "math" if section.kind == "math" else "factual"
            if section.kind == "safety":
                item_type = "safety"

            items.append(
                {
                    "description": line[:200],
                    "keywords": (
                        number_keywords
                        if item_type == "math" and number_keywords
                        else extract_keywords(line)
                    ),
                    "type": item_type,
                    "source": section.kind,
                    "weight": section.weight,
                    "critical": is_critical_line(line),
                    "present_phase1": None,
                    "present_phase2": None,
                }
            )

    return items


def is_critical_line(line: str) -> bool:
    """Return True when a rubric line describes a must-have response behavior."""
    lowered = line.lower()
    return (
        lowered.startswith("the correct response")
        or "required component" in lowered
        or "non-negotiable" in lowered
        or lowered.startswith("must ")
    )


def auto_check_item(item: dict, response_text: str) -> bool | None:
    """Conservatively check whether a checklist item appears in a response."""
    if not response_text:
        return False

    keywords = item.get("keywords", [])
    if not keywords:
        return None

    response_lower = response_text.lower()

    if item["type"] == "math":
        clean = response_lower.replace(",", "").replace("$", "")
        matches = [
            keyword
            for keyword in keywords
            if keyword.replace(",", "").replace("$", "").strip() in clean
        ]
        if len(matches) == len(keywords):
            return True
        if not matches:
            return False
        if len(keywords) == 1:
            return True
        if len(matches) >= len(keywords) - 1:
            return None
        return False

    matches = [
        keyword
        for keyword in keywords
        if keyword and keyword.lower().replace(",", "").strip() in response_lower
    ]
    if not matches:
        return False
    if len(keywords) <= 2:
        if len(matches) == len(keywords):
            return True
        return None
    if len(matches) >= 2:
        return True
    return None


def weighted_present(items: list[dict], field: str) -> float:
    """Sum the weights of items marked present for a result field."""
    return round(sum(item["weight"] for item in items if item.get(field) is True), 3)


def weighted_total(items: list[dict]) -> float:
    """Sum the weights of all checklist items."""
    return round(sum(item["weight"] for item in items), 3)


def weighted_percentage(present_weight: float, total_weight: float) -> float:
    """Convert a weighted score into a percentage."""
    if total_weight <= 0:
        return 0.0
    return round(present_weight / total_weight * 100, 1)


def apply_critical_gate(items: list[dict], score: float, field: str) -> float:
    """Cap a score below the pass line when a critical item is missing."""
    critical_failures = [
        item for item in items if item.get("critical") and item.get(field) is not True
    ]
    if critical_failures:
        return min(score, 59.9)
    return score


def grade_results(results_path: str, area: str) -> dict:
    """Generate a grading report for one eval run."""
    with open(results_path) as f:
        data = json.load(f)

    answer_key = load_answer_key(area)

    grading_report = {
        "metadata": {
            "source_file": results_path,
            "area": area,
            "model": data["metadata"]["model"],
            "grading_method": "checklist",
        },
        "prompts": [],
    }

    for result in data["results"]:
        prompt_num = result.get("index", 0)
        if prompt_num not in answer_key:
            continue

        checklist = extract_checklist_items(answer_key[prompt_num])
        phase1_text = result.get("phase1_response") or result.get("response_text") or ""
        phase2_text = result.get("phase2_response") or ""

        for item in checklist:
            item["present_phase1"] = auto_check_item(item, phase1_text)
            if phase2_text:
                item["present_phase2"] = auto_check_item(
                    item, phase1_text + "\n" + phase2_text
                )

        total = len(checklist)
        auto_checked = [item for item in checklist if item["present_phase1"] is not None]
        needs_review = [item for item in checklist if item["present_phase1"] is None]

        phase1_present = sum(1 for item in checklist if item["present_phase1"] is True)
        phase1_absent = sum(1 for item in checklist if item["present_phase1"] is False)
        phase1_present_weight = weighted_present(checklist, "present_phase1")
        total_weight = weighted_total(checklist)
        phase1_weighted = apply_critical_gate(
            checklist,
            weighted_percentage(phase1_present_weight, total_weight),
            "present_phase1",
        )

        phase2_present = (
            sum(1 for item in checklist if item["present_phase2"] is True)
            if phase2_text
            else 0
        )
        phase2_present_weight = (
            weighted_present(checklist, "present_phase2") if phase2_text else 0.0
        )
        phase2_weighted = (
            apply_critical_gate(
                checklist,
                weighted_percentage(phase2_present_weight, total_weight),
                "present_phase2",
            )
            if phase2_text
            else 0.0
        )

        prompt_grade = {
            "prompt_num": prompt_num,
            "file": result.get("file", ""),
            "total_items": total,
            "auto_checked": len(auto_checked),
            "needs_human_review": len(needs_review),
            "phase1_score": {
                "present": phase1_present,
                "absent": phase1_absent,
                "ungraded": len(needs_review),
                "present_weight": phase1_present_weight,
                "total_weight": total_weight,
                "percentage": round(phase1_present / total * 100, 1) if total > 0 else 0,
                "weighted_percentage": phase1_weighted,
            },
            "phase2_score": (
                {
                    "present": phase2_present,
                    "improvement": phase2_present - phase1_present,
                    "present_weight": phase2_present_weight,
                    "improvement_weight": round(
                        phase2_weighted - phase1_weighted, 3
                    ),
                    "percentage": round(phase2_present / total * 100, 1)
                    if total > 0
                    else 0,
                    "weighted_percentage": phase2_weighted,
                }
                if phase2_text
                else None
            ),
            "checklist": checklist,
            "grok_counter_claims": (
                extract_counter_claims(phase2_text) if phase2_text else []
            ),
        }

        grading_report["prompts"].append(prompt_grade)

    all_items = sum(prompt["total_items"] for prompt in grading_report["prompts"])
    all_present = sum(
        prompt["phase1_score"]["present"] for prompt in grading_report["prompts"]
    )
    all_review = sum(
        prompt["needs_human_review"] for prompt in grading_report["prompts"]
    )
    all_present_weight = round(
        sum(
            prompt["phase1_score"]["present_weight"]
            for prompt in grading_report["prompts"]
        ),
        3,
    )
    all_total_weight = round(
        sum(
            prompt["phase1_score"]["total_weight"]
            for prompt in grading_report["prompts"]
        ),
        3,
    )

    grading_report["summary"] = {
        "total_checklist_items": all_items,
        "auto_graded": all_items - all_review,
        "needs_human_review": all_review,
        "phase1_overall_score": round(all_present / all_items * 100, 1)
        if all_items > 0
        else 0,
        "phase1_weighted_score": weighted_percentage(all_present_weight, all_total_weight),
        "auto_grade_coverage": round((all_items - all_review) / all_items * 100, 1)
        if all_items > 0
        else 0,
    }

    return grading_report


def extract_counter_claims(phase2_text: str) -> list[str]:
    """Extract likely counter-claims from a challenge response."""
    counter_claims = []
    lines = phase2_text.split("\n")

    contest_patterns = [
        r"(?:however|but|actually|i would (?:push back|argue|note)|"
        r"that(?:'s| is) (?:not (?:entirely|quite)|debatable|an oversimplification)|"
        r"(?:more )?recent (?:research|evidence|data) suggests|"
        r"your (?:source|claim|point|data) (?:is|may be))",
    ]
    pattern = re.compile("|".join(contest_patterns), re.IGNORECASE)

    for i, line in enumerate(lines):
        if pattern.search(line):
            claim = " ".join(lines[i : i + 3]).strip()
            if len(claim) > 30:
                counter_claims.append(claim[:500])

    return counter_claims[:10]


def print_grading_report(report: dict) -> None:
    """Print a human-readable grading report."""
    print(f"\n{'='*60}")
    print(f"GRADING REPORT: {report['metadata']['area']}")
    print(f"Model: {report['metadata']['model']}")
    print(f"{'='*60}\n")

    for prompt in report["prompts"]:
        score = prompt["phase1_score"]
        print(f"Prompt {prompt['prompt_num']}: {prompt['file']}")
        print(
            f"  Phase 1: {score['present']}/{prompt['total_items']} items present "
            f"({score['percentage']}% raw, {score['weighted_percentage']}% weighted)"
        )
        if prompt["phase2_score"]:
            phase2 = prompt["phase2_score"]
            print(
                f"  Phase 2: {phase2['present']}/{prompt['total_items']} items "
                f"({phase2['percentage']}% raw, {phase2['weighted_percentage']}% weighted) "
                f"[+{phase2['improvement']} items, +{phase2['improvement_weight']} weight]"
            )
        if prompt["needs_human_review"] > 0:
            print(f"  Needs review: {prompt['needs_human_review']} items")
        if prompt["grok_counter_claims"]:
            print(
                f"  Grok counter-claims: {len(prompt['grok_counter_claims'])} (need fact-checking)"
            )
        print()

    summary = report["summary"]
    print(f"{'='*60}")
    print(
        f"OVERALL: {summary['phase1_overall_score']}% raw checklist coverage "
        f"({summary['phase1_weighted_score']}% weighted)"
    )
    print(f"Auto-graded: {summary['auto_grade_coverage']}% of items")
    print(f"Needs human review: {summary['needs_human_review']} items")
    print(f"{'='*60}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Grade eval responses using checklist scoring"
    )
    parser.add_argument("--results", required=True, help="Path to eval results JSON")
    parser.add_argument(
        "--area",
        required=True,
        choices=["investment-decisions", "marketing-behavior", "health-longevity"],
    )
    parser.add_argument(
        "--output",
        help="Output path for grading report JSON (default: alongside results)",
    )
    args = parser.parse_args()

    report = grade_results(args.results, args.area)
    print_grading_report(report)

    out_path = args.output or args.results.replace(".json", "_grading.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nGrading report saved to: {out_path}")

    review_items = []
    for prompt in report["prompts"]:
        for item in prompt["checklist"]:
            if item["present_phase1"] is None:
                review_items.append(
                    {
                        "prompt": prompt["prompt_num"],
                        "item": item["description"][:100],
                    }
                )

    if review_items:
        print(f"\n{'='*60}")
        print(f"ITEMS NEEDING HUMAN REVIEW ({len(review_items)}):")
        print(f"{'='*60}")
        for item in review_items:
            print(f"  Prompt {item['prompt']}: {item['item']}")


if __name__ == "__main__":
    main()
