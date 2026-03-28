from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(v.strip()) for v in inner.split(",")]
    if value.isdigit():
        return int(value)
    return value.strip('"').strip("'")


def _load_simple_yaml(path: str | Path) -> dict[str, Any]:
    result: dict[str, Any] = {}
    current_key: str | None = None

    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        stripped = line.strip()
        if stripped.startswith("- ") and current_key:
            result.setdefault(current_key, []).append(_parse_scalar(stripped[2:]))
            continue

        if ":" in stripped:
            key, val = stripped.split(":", 1)
            key = key.strip()
            val = val.strip()
            if val == "":
                result[key] = []
                current_key = key
            else:
                result[key] = _parse_scalar(val)
                current_key = key

    return result


@dataclass
class RuleEngine:
    exclusion_rules: dict[str, Any]
    grade_mode: dict[str, Any]

    @classmethod
    def from_files(cls, exclusion_path: str | Path, grade_mode_path: str | Path) -> "RuleEngine":
        exclusion = _load_simple_yaml(exclusion_path)
        grade_mode = _load_simple_yaml(grade_mode_path)
        return cls(exclusion_rules=exclusion, grade_mode=grade_mode)

    def apply(self, parsed_sections: dict[str, list[dict]]) -> dict[str, Any]:
        include_years = set(self.grade_mode.get("include_only_years", []))
        filtered: dict[str, list[dict]] = {}
        masked_patterns = [re.compile(p) for p in self.exclusion_rules.get("mask_patterns", [])]
        excluded_keywords = self.exclusion_rules.get("exclude_as_core_evidence_keywords", [])

        for section, items in parsed_sections.items():
            new_items: list[dict] = []
            for item in items:
                if include_years and item.get("year") and item["year"] not in include_years:
                    continue

                text = item["text"]
                for pat in masked_patterns:
                    text = pat.sub("[MASKED]", text)

                if any(keyword in text for keyword in excluded_keywords):
                    continue

                cloned = dict(item)
                cloned["text"] = text
                new_items.append(cloned)

            filtered[section] = new_items

        return {
            "target_grade": self.grade_mode["target_grade"],
            "focus_year": self.grade_mode["focus_year"],
            "axes": self.grade_mode.get("default_axis", []),
            "allow_axis4": self.grade_mode.get("allow_axis4", False),
            "sections": filtered,
        }
