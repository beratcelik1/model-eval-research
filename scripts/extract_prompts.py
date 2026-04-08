"""Extract prompts from area README.md files into individual .md files."""

from __future__ import annotations

import argparse
from pathlib import Path

from eval_schema import extract_prompts_from_readme

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AREAS = ["investment-decisions", "marketing-behavior", "health-longevity"]


def slugify(text: str) -> str:
    """Turn a prompt title into a filename-safe slug."""
    import re

    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def save_prompts(area: str, prompts: list) -> list[Path]:
    """Save extracted prompts as individual .md files."""
    out_dir = PROJECT_ROOT / "areas" / area / "prompts"
    out_dir.mkdir(parents=True, exist_ok=True)

    saved = []
    for p in prompts:
        num = str(p.number).zfill(2)
        slug = slugify(p.title)
        filename = f"{num}-{slug}.md"
        filepath = out_dir / filename

        content_parts = [p.prompt_text]

        if p.what_it_tests:
            content_parts.append(f"\n---\nWhat it tests: {p.what_it_tests}")

        if p.scoring:
            content_parts.append(f"\n---\nScoring:\n{p.scoring}")

        content_parts.append(f"\n---\nCategory: {p.category}\nPrompt: {p.number}")

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
