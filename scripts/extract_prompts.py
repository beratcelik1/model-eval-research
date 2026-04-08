"""Extract prompts from area README.md files into individual .md files.

Reads each area's README.md, finds "Paste into Grok:" blocks, and saves
each prompt as a separate file in areas/{area}/prompts/.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AREAS = ["investment-decisions", "marketing-behavior", "health-longevity"]


def slugify(text: str) -> str:
    """Turn a prompt title into a filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def extract_prompts_from_readme(readme_path: Path) -> list[dict[str, str]]:
    """Parse a README.md and extract prompt blocks.

    Looks for sections like:
        #### PROMPT N -- Title [CATEGORY]
        **Paste into Grok:**
        > prompt text here

    Also extracts "What it tests:" and "Scoring:" sections for metadata.
    """
    text = readme_path.read_text()

    # Split by prompt headers
    prompt_pattern = re.compile(
        r"####\s+PROMPT\s+(\d+)\s*[—–-]+\s*(.+?)(?:\n|$)",
        re.IGNORECASE,
    )

    matches = list(prompt_pattern.finditer(text))
    if not matches:
        return []

    prompts = []
    for i, match in enumerate(matches):
        number = int(match.group(1))
        title_raw = match.group(2).strip()

        # Extract category from brackets like [CORE] or [EDGE CASE]
        cat_match = re.search(r"\[([^\]]+)\]", title_raw)
        category = cat_match.group(1) if cat_match else "CORE"
        title = re.sub(r"\s*\[[^\]]+\]\s*", "", title_raw).strip()

        # Get the section text between this prompt and the next
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[start:end]

        # Extract the "Paste into Grok:" block
        grok_match = re.search(
            r"\*\*Paste into Grok:\*\*\s*\n((?:>\s*.+\n?)+)",
            section,
        )
        if not grok_match:
            continue

        # Clean the blockquote: strip leading "> " from each line
        raw_prompt = grok_match.group(1)
        prompt_lines = []
        for line in raw_prompt.strip().split("\n"):
            cleaned = re.sub(r"^>\s?", "", line)
            prompt_lines.append(cleaned)
        prompt_text = "\n".join(prompt_lines).strip()

        # Extract "What it tests:"
        tests_match = re.search(
            r"\*\*What it tests:\*\*\s*(.+?)(?:\n\n|\n\*\*)",
            section,
            re.DOTALL,
        )
        what_it_tests = tests_match.group(1).strip() if tests_match else ""

        # Extract scoring table
        scoring_match = re.search(
            r"\*\*Scoring:\*\*\s*\n((?:\|.+\n)+)",
            section,
        )
        scoring = scoring_match.group(1).strip() if scoring_match else ""

        prompts.append(
            {
                "number": number,
                "title": title,
                "category": category,
                "prompt_text": prompt_text,
                "what_it_tests": what_it_tests,
                "scoring": scoring,
            }
        )

    return prompts


def save_prompts(area: str, prompts: list[dict[str, str]]) -> list[Path]:
    """Save extracted prompts as individual .md files."""
    out_dir = PROJECT_ROOT / "areas" / area / "prompts"
    out_dir.mkdir(parents=True, exist_ok=True)

    saved = []
    for p in prompts:
        num = str(p["number"]).zfill(2)
        slug = slugify(p["title"])
        filename = f"{num}-{slug}.md"
        filepath = out_dir / filename

        content_parts = [p["prompt_text"]]

        if p["what_it_tests"]:
            content_parts.append(f"\n---\nWhat it tests: {p['what_it_tests']}")

        if p["scoring"]:
            content_parts.append(f"\n---\nScoring:\n{p['scoring']}")

        content_parts.append(f"\n---\nCategory: {p['category']}\nPrompt: {p['number']}")

        filepath.write_text("\n".join(content_parts) + "\n")
        saved.append(filepath)

    return saved


def run_extract(areas: list[str]) -> None:
    """Extract prompts for the given areas."""
    for area in areas:
        readme = PROJECT_ROOT / "areas" / area / "README.md"
        if not readme.exists():
            print(f"SKIP: {readme} not found")
            continue

        print(f"Extracting from: {area}")
        prompts = extract_prompts_from_readme(readme)

        if not prompts:
            print(f"  No prompts found in {readme}")
            continue

        saved = save_prompts(area, prompts)
        print(f"  Saved {len(saved)} prompts:")
        for s in saved:
            print(f"    {s.name}")
    print()
    print("Done. Run 'python scripts/run_eval.py --mode validate --area <area>' next.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract prompts from area README.md files"
    )
    parser.add_argument(
        "--area",
        choices=AREAS,
        help="Extract from one area (default: all)",
    )
    args = parser.parse_args()

    target_areas = [args.area] if args.area else AREAS
    run_extract(target_areas)


if __name__ == "__main__":
    main()
