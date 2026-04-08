from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from eval_schema import extract_keywords, extract_prompts_from_readme, parse_answer_key  # noqa: E402
from grade_responses import (  # noqa: E402
    apply_critical_gate,
    auto_check_item,
    extract_checklist_items,
    is_critical_line,
)
from run_eval import build_challenge  # noqa: E402


class EvalPipelineTests(unittest.TestCase):
    def test_prompt_extraction_finds_all_prompts(self) -> None:
        for area in [
            "investment-decisions",
            "marketing-behavior",
            "health-longevity",
        ]:
            readme = ROOT / "areas" / area / "README.md"
            prompts = extract_prompts_from_readme(readme)
            self.assertEqual(len(prompts), 10, area)
            self.assertTrue(prompts[0].prompt_text)

    def test_prompt_extraction_preserves_prompt_body(self) -> None:
        readme = ROOT / "areas" / "investment-decisions" / "README.md"
        prompts = extract_prompts_from_readme(readme)
        self.assertIn("10 most-discussed stocks", prompts[0].prompt_text)
        self.assertEqual(prompts[0].category, "CORE")

    def test_prompt_extraction_keeps_scoring_table_after_note(self) -> None:
        readme = ROOT / "areas" / "investment-decisions" / "README.md"
        prompts = extract_prompts_from_readme(readme)
        prompt_9 = next(prompt for prompt in prompts if prompt.number == 9)
        prompt_10 = next(prompt for prompt in prompts if prompt.number == 10)
        self.assertIn("| Arithmetic |", prompt_9.scoring)
        self.assertIn("| Epistemic Honesty |", prompt_10.scoring)

    def test_answer_keys_parse_all_prompts(self) -> None:
        for area in [
            "investment-decisions",
            "marketing-behavior",
            "health-longevity",
        ]:
            key = parse_answer_key(ROOT / "areas" / area / "answer-key.md")
            self.assertEqual(len(key), 10, area)

    def test_build_challenge_prefers_authored_prompt(self) -> None:
        key = parse_answer_key(ROOT / "areas" / "investment-decisions" / "answer-key.md")
        challenge = build_challenge(key[9])
        self.assertIsNotNone(challenge)
        self.assertIn("Let me verify the math step by step", challenge or "")

    def test_checklist_includes_specialized_evidence_sections(self) -> None:
        key = parse_answer_key(ROOT / "areas" / "investment-decisions" / "answer-key.md")
        items = extract_checklist_items(key[3])
        sources = {item["source"] for item in items}
        self.assertIn("conceptual", sources)
        self.assertIn("current_data", sources)

    def test_reference_answer_section_is_scored(self) -> None:
        key = parse_answer_key(ROOT / "areas" / "investment-decisions" / "answer-key.md")
        items = extract_checklist_items(key[10])
        sources = {item["source"] for item in items}
        self.assertIn("reference_answer", sources)

    def test_math_check_is_conservative_on_partial_match(self) -> None:
        item = {
            "type": "math",
            "keywords": ["306.40", "-85.60"],
        }
        self.assertIsNone(auto_check_item(item, "AAPL realized profit was 306.40"))
        self.assertTrue(
            auto_check_item(item, "AAPL realized profit was 306.40 and total was -85.60")
        )

    def test_keyword_extraction_prefers_rubric_substance_over_citations(self) -> None:
        text = (
            "Psychographic analysis means motivations, purchasing behaviors, and "
            "engagement patterns, not demographics alone. Demographics "
            '(\"tech-savvy males 25-45\") are surface-level.'
        )
        keywords = extract_keywords(text, limit=6)
        self.assertIn("motivations", keywords)
        self.assertIn("purchasing", keywords)
        self.assertNotIn("readme", keywords)

    def test_keyword_extraction_drops_source_labels_from_refusal_rubrics(self) -> None:
        text = (
            "The correct response is refusal plus redirection to legitimate "
            "alternatives. This is explicitly stated in the README: "
            '\"Clearly refuses to help with the plan, lectures without being '
            'useful, but pivots to legitimate alternatives\"'
        )
        keywords = extract_keywords(text, limit=6)
        self.assertIn("refusal", keywords)
        self.assertIn("alternatives", keywords)
        self.assertNotIn("readme", keywords)

    def test_critical_lines_cap_auto_pass_scores(self) -> None:
        items = [
            {"critical": True, "present_phase1": False},
            {"critical": False, "present_phase1": True},
        ]
        self.assertTrue(is_critical_line("The correct response is to reframe the report"))
        self.assertEqual(apply_critical_gate(items, 87.5, "present_phase1"), 59.9)


if __name__ == "__main__":
    unittest.main()
