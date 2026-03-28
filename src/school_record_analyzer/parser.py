from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


SECTION_PATTERNS = {
    "subject_scores": re.compile(r"^(교과성적|성적)", re.IGNORECASE),
    "subject_details": re.compile(r"^(세특|교과세특)", re.IGNORECASE),
    "creative_activities": re.compile(r"^(창체|창의적\s*체험활동)", re.IGNORECASE),
    "behavioral_notes": re.compile(r"^(행특|행동특성)", re.IGNORECASE),
    "attendance": re.compile(r"^(출결)", re.IGNORECASE),
}


@dataclass
class ParsedRecord:
    sections: dict[str, list[dict]]
    raw_lines: list[str]


def _read_text(path: Path) -> str:
    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".pdf":
        try:
            import pypdf  # type: ignore
        except ImportError as exc:
            raise RuntimeError("PDF 파싱을 위해 pypdf 설치가 필요합니다.") from exc
        reader = pypdf.PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    raise ValueError(f"지원하지 않는 확장자: {path.suffix}")


def parse_record_file(path: str | Path) -> ParsedRecord:
    p = Path(path)
    text = _read_text(p)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    sections = {key: [] for key in SECTION_PATTERNS}
    current = None

    for idx, line in enumerate(lines, start=1):
        switched = False
        for section, pattern in SECTION_PATTERNS.items():
            if pattern.search(line):
                current = section
                switched = True
                break
        if switched:
            continue
        if current is None:
            continue

        year_match = re.search(r"(\d)학년", line)
        semester_match = re.search(r"(\d)학기", line)

        item = {
            "text": line,
            "source_lines": [idx],
        }
        if year_match:
            item["year"] = int(year_match.group(1))
        if semester_match:
            item["semester"] = int(semester_match.group(1))
        sections[current].append(item)

    return ParsedRecord(sections=sections, raw_lines=lines)
