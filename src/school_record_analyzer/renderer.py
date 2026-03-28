from __future__ import annotations

from pathlib import Path
from typing import Any


def _join_evidence(items: list[dict], prefix: str) -> str:
    if not items:
        return "- 근거 없음"
    lines = []
    for item in items:
        src = ",".join(map(str, item.get("source_lines", [])))
        lines.append(f"- {prefix} 해석: {item['text']} (근거: 원문 {src}행)")
    return "\n".join(lines)


def render_report(payload: dict[str, Any], template_path: str | Path) -> str:
    template = Path(template_path).read_text(encoding="utf-8")
    sections = payload["sections"]

    academic = _join_evidence(sections.get("subject_scores", []) + sections.get("subject_details", []), "학업역량")
    career = _join_evidence(sections.get("creative_activities", []), "진로역량")
    community = _join_evidence(sections.get("behavioral_notes", []), "공동체역량")
    attendance = _join_evidence(sections.get("attendance", []), "출결")

    axis4 = "- 4축 재서술 비활성화"
    if payload.get("allow_axis4"):
        axis4 = _join_evidence(sections.get("subject_details", []), "4축(자기주도성)")

    rendered = (
        template.replace("{{target_grade}}", str(payload["target_grade"]))
        .replace("{{focus_year}}", str(payload["focus_year"]))
        .replace("{{academic_section}}", academic)
        .replace("{{career_section}}", career)
        .replace("{{community_section}}", community)
        .replace("{{axis4_section}}", axis4)
        .replace("{{attendance_summary}}", attendance)
    )
    return rendered
