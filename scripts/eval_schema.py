"""Shared parsing helpers for prompts and answer keys.

These helpers keep the repository's markdown contract in one place so the
extractor, eval runner, and grader all interpret the source material the same
way.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path


PROMPT_HEADER_RE = re.compile(
    r"^####\s+PROMPT\s+(\d+)\s*[-–]+\s*(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
ANSWER_KEY_HEADER_RE = re.compile(
    r"^#{2,3}\s+Prompt\s+(\d+)(?::\s*(.+?))?\s*$",
    re.IGNORECASE | re.MULTILINE,
)
SECTION_HEADER_RE = re.compile(r"^\*\*(.+?)\*\*\s*$", re.MULTILINE)

CHECKLIST_SECTION_KINDS = {
    "verified",
    "conceptual",
    "current_data",
    "core_insight",
    "supporting_evidence",
    "contextual_data",
    "safety",
    "math",
    "reference_answer",
}

CHECKLIST_SECTION_WEIGHTS = {
    "verified": 1.0,
    "conceptual": 1.25,
    "current_data": 0.5,
    "core_insight": 1.5,
    "supporting_evidence": 0.75,
    "contextual_data": 0.75,
    "safety": 1.5,
    "math": 1.0,
    "reference_answer": 1.0,
}

CHECKLIST_KIND_ALIASES = (
    ("verified correct benchmarks", "verified"),
    ("conceptual understanding", "conceptual"),
    ("requires current data", "current_data"),
    ("core contrarian insight", "core_insight"),
    ("core insight", "core_insight"),
    ("supporting academic evidence", "supporting_evidence"),
    ("contextual data points", "contextual_data"),
    ("safety benchmarks", "safety"),
    ("pure math/logic", "math"),
    ("exact calculations", "math"),
    ("formula", "math"),
    ('the "correct answer" for this prompt', "reference_answer"),
    ("the correct answer for this prompt", "reference_answer"),
    ("judgment-based criteria", "judgment"),
    ("debatable points", "debatable"),
    ("challenge prompt", "challenge"),
    ("common errors to watch for", "common_errors"),
    ("breakdown summary", "math"),
    ("the prompt provides", "context"),
)

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "could",
    "do",
    "does",
    "for",
    "from",
    "good",
    "how",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "may",
    "more",
    "most",
    "must",
    "needs",
    "no",
    "not",
    "of",
    "on",
    "or",
    "our",
    "out",
    "response",
    "should",
    "so",
    "than",
    "that",
    "the",
    "their",
    "them",
    "there",
    "these",
    "this",
    "to",
    "use",
    "user",
    "valid",
    "well",
    "what",
    "when",
    "which",
    "with",
}

GENERIC_KEYWORDS = {
    "analysis",
    "answer",
    "benchmark",
    "claim",
    "correct",
    "criteria",
    "data",
    "evidence",
    "good",
    "guide",
    "item",
    "judge",
    "judgment",
    "model",
    "note",
    "optional",
    "pattern",
    "point",
    "prompt",
    "quality",
    "question",
    "real",
    "report",
    "required",
    "research",
    "response",
    "score",
    "scoring",
    "section",
    "stated",
    "source",
    "specific",
    "study",
    "thing",
    "valid",
    "value",
    "wrong",
    "means",
    "explicitly",
    "clearly",
    "describing",
    "describe",
    "description",
    "psychographic",
    "demographics",
    "readme",
    "prompt",
    "report",
    "documentation",
    "edition",
    "dm",
    "plus",
    "alone",
}

SOURCE_LIKE_TERMS = {
    "benchmark",
    "benchmarks",
    "book",
    "citation",
    "citations",
    "cfr",
    "documentation",
    "edition",
    "guide",
    "guides",
    "kb",
    "paper",
    "part",
    "pmid",
    "prompt",
    "readme",
    "report",
    "reports",
    "research",
    "revised",
    "source",
    "sources",
    "study",
    "title",
}


@dataclass(frozen=True)
class PromptDoc:
    """One prompt parsed from a README."""

    number: int
    title: str
    category: str
    prompt_text: str
    what_it_tests: str
    scoring: str


@dataclass(frozen=True)
class KeySection:
    """A parsed section inside an answer key prompt."""

    title: str
    body: str
    kind: str
    weight: float


@dataclass(frozen=True)
class AnswerKeyPrompt:
    """A parsed prompt entry inside an answer key."""

    number: int
    title: str
    sections: list[KeySection]

    def sections_by_kind(self, *kinds: str) -> list[KeySection]:
        allowed = set(kinds)
        return [section for section in self.sections if section.kind in allowed]

    def first_challenge_text(self) -> str | None:
        for section in self.sections:
            if section.kind == "challenge":
                text = strip_blockquote(section.body.strip())
                if text:
                    return text
        return None

    def evidence_sections(self) -> list[KeySection]:
        return [
            section
            for section in self.sections
            if section.kind in CHECKLIST_SECTION_KINDS
        ]


def split_markdown_blocks(text: str, header_re: re.Pattern[str]) -> list[tuple[int, str, str]]:
    """Split markdown text into numbered blocks using an anchored header regex."""
    matches = list(header_re.finditer(text))
    blocks: list[tuple[int, str, str]] = []
    for i, match in enumerate(matches):
        number = int(match.group(1))
        title = (match.group(2) or "").strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks.append((number, title, text[start:end].strip()))
    return blocks


def extract_prompts_from_readme(readme_path: Path) -> list[PromptDoc]:
    """Parse all prompt definitions from an area README."""
    text = readme_path.read_text()
    prompts: list[PromptDoc] = []

    for number, title_raw, body in split_markdown_blocks(text, PROMPT_HEADER_RE):
        cat_match = re.search(r"\[([^\]]+)\]", title_raw)
        category = cat_match.group(1).strip() if cat_match else "CORE"
        title = re.sub(r"\s*\[[^\]]+\]\s*", "", title_raw).strip()

        prompt_text = extract_blockquote_after_label(body, "**Paste into Grok:**")
        if not prompt_text:
            continue

        what_it_tests = extract_inline_markdown_field(body, "What it tests")
        scoring = extract_table_after_label(body, "Scoring")

        prompts.append(
            PromptDoc(
                number=number,
                title=title,
                category=category,
                prompt_text=prompt_text,
                what_it_tests=what_it_tests,
                scoring=scoring,
            )
        )

    return prompts


def parse_answer_key(path: Path) -> dict[int, AnswerKeyPrompt]:
    """Parse an answer key markdown file into structured prompt entries."""
    text = path.read_text()
    prompts: dict[int, AnswerKeyPrompt] = {}

    for number, title, body in split_markdown_blocks(text, ANSWER_KEY_HEADER_RE):
        sections = parse_key_sections(body)
        prompts[number] = AnswerKeyPrompt(number=number, title=title, sections=sections)

    return prompts


def parse_key_sections(body: str) -> list[KeySection]:
    """Parse bold markdown headings inside one answer-key prompt body."""
    matches = list(SECTION_HEADER_RE.finditer(body))
    if not matches:
        return []

    sections: list[KeySection] = []
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        kind = classify_section(title)
        sections.append(
            KeySection(
                title=title,
                body=content,
                kind=kind,
                weight=CHECKLIST_SECTION_WEIGHTS.get(kind, 1.0),
            )
        )

    return sections


def classify_section(title: str) -> str:
    """Map a human heading to a stable internal section kind."""
    normalized = title.strip().strip(":").lower()

    for prefix, kind in CHECKLIST_KIND_ALIASES:
        if normalized.startswith(prefix):
            return kind

    if normalized.endswith("stock position") or "covered call" in normalized:
        return "math"
    if "realized p&l" in normalized:
        return "math"
    if "correct answer" in normalized:
        return "reference_answer"

    return "other"


def extract_inline_markdown_field(text: str, label: str) -> str:
    """Extract a single-line markdown field like '**What it tests:** value'."""
    pattern = re.compile(
        rf"^\*\*{re.escape(label)}:\*\*\s*(.+?)\s*$",
        re.IGNORECASE | re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def extract_table_after_label(text: str, label: str) -> str:
    """Extract the first markdown table that appears after a bold label."""
    lines = text.splitlines()
    collecting = False
    table_started = False
    collected: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not collecting:
            if stripped == f"**{label}:**":
                collecting = True
            continue

        if stripped.startswith("**") and stripped.endswith("**") and not table_started:
            return ""
        if stripped.startswith("|"):
            table_started = True
            collected.append(stripped)
            continue
        if table_started:
            break

    return "\n".join(collected).strip()


def extract_blockquote_after_label(text: str, label: str) -> str:
    """Extract the blockquote lines immediately after a label."""
    lines = text.splitlines()
    collecting = False
    collected: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not collecting:
            if stripped == label:
                collecting = True
            continue

        if stripped.startswith(">"):
            collected.append(re.sub(r"^>\s?", "", stripped))
            continue

        if stripped == "" and collected:
            break
        if stripped:
            break

    return "\n".join(collected).strip()


def strip_blockquote(text: str) -> str:
    """Remove markdown blockquote prefixes from a block of text."""
    if not text:
        return ""
    return "\n".join(re.sub(r"^>\s?", "", line) for line in text.splitlines()).strip()


def iter_checklist_lines(section: KeySection) -> list[str]:
    """Extract bullet or numbered checklist items from a section."""
    items: list[str] = []
    for raw_line in section.body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- ") or line.startswith("* "):
            items.append(line[2:].strip())
            continue
        if re.match(r"^\d+\.\s+", line):
            items.append(re.sub(r"^\d+\.\s+", "", line))
    return items


def extract_keywords(text: str, limit: int = 4) -> list[str]:
    """Extract conservative matching keywords from one checklist line."""
    cleaned = re.sub(r"\[[^\]]*\]", "", text)
    cleaned = re.sub(
        r"\(([^()]*)\)",
        lambda match: normalize_parenthetical(match.group(1)),
        cleaned,
    )
    candidates: list[str] = []

    for phrase in re.findall(r'"([^"]{3,80})"', cleaned):
        normalized = normalize_phrase(phrase)
        word_count = len(normalized.split())
        if (
            0 < word_count <= 4
            and normalized
            and normalized not in STOPWORDS
            and not looks_like_source_phrase(normalized)
            and not re.search(r"\d", normalized)
            and not normalized.startswith("sorry ")
        ):
            candidates.append(normalized)

    for phrase in re.findall(
        r"\b[A-Z][A-Za-z0-9+/.-]*(?:\s+[A-Z][A-Za-z0-9+/.-]*)*\b", cleaned
    ):
        normalized = normalize_phrase(phrase)
        if (
            normalized
            and normalized not in STOPWORDS
            and not looks_like_source_phrase(normalized)
            and is_informative_entity_phrase(phrase, normalized)
        ):
            candidates.append(normalized)

    words = []
    for match in re.finditer(r"[A-Za-z][A-Za-z0-9+/-]{3,}", cleaned):
        raw_word = match.group(0)
        normalized = normalize_phrase(raw_word)
        suffix = cleaned[match.end() : match.end() + 2]
        if (
            not normalized
            or normalized in STOPWORDS
            or normalized in GENERIC_KEYWORDS
            or looks_like_source_phrase(normalized)
            or (raw_word[0].isupper() and not raw_word.isupper() and suffix == "'s")
        ):
            continue
        words.append(normalized)

    candidates.extend(words)

    for size in (2,):
        for i in range(len(words) - size + 1):
            phrase = " ".join(words[i : i + size])
            if any(part in GENERIC_KEYWORDS for part in phrase.split()):
                continue
            candidates.append(phrase)

    result: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        result.append(candidate)
        if len(result) >= limit:
            break
    return result


def normalize_phrase(text: str) -> str:
    """Normalize a candidate keyword or phrase for substring matching."""
    phrase = text.strip().lower()
    phrase = re.sub(r"[^a-z0-9+/%.\-\s]", "", phrase)
    phrase = re.sub(r"\s+", " ", phrase)
    return phrase.strip()


def looks_like_source_phrase(text: str) -> bool:
    """Return True when a candidate is mostly a citation or source label."""
    words = normalize_phrase(text).split()
    if not words:
        return True

    meaningful = [word for word in words if word not in {"the", "a", "an", "of", "and"}]
    if not meaningful:
        return True

    if any(word in SOURCE_LIKE_TERMS for word in meaningful):
        return True

    return False


def is_informative_entity_phrase(raw_phrase: str, normalized: str) -> bool:
    """Keep short entity-like phrases that can plausibly appear in responses."""
    if len(normalized.split()) > 3:
        return False
    if normalized.startswith("the "):
        tail = normalized.split()[1:]
        if len(tail) == 1 and len(tail[0]) <= 2:
            return False
    if re.search(r"\d", normalized):
        return True
    tokens = raw_phrase.split()
    return any(
        token.isupper() or any(char.isdigit() for char in token) or "/" in token
        for token in tokens
    )


def normalize_parenthetical(text: str) -> str:
    """Keep substantive parentheticals while dropping citation-style ones."""
    normalized = normalize_phrase(text)
    if not normalized:
        return " "
    if looks_like_source_phrase(normalized):
        return " "
    if re.search(r"\b(?:19|20)\d{2}\b", normalized):
        return " "
    return f" {text} "
