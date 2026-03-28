from pathlib import Path

from school_record_analyzer.parser import parse_record_file
from school_record_analyzer.renderer import render_report
from school_record_analyzer.rules import RuleEngine

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FIXTURES = ROOT / "tests" / "fixtures"
GOLDEN = ROOT / "tests" / "golden"


def _run_pipeline(path: Path) -> str:
    parsed = parse_record_file(path)
    engine = RuleEngine.from_files(DOCS / "exclusion_rules.yaml", DOCS / "grade2_mode.yaml")
    payload = engine.apply(parsed.sections)
    return render_report(payload, DOCS / "report_template.md")


def test_parser_section_split():
    parsed = parse_record_file(FIXTURES / "record_a.txt")
    assert len(parsed.sections["subject_scores"]) == 2
    assert len(parsed.sections["subject_details"]) == 1
    assert len(parsed.sections["creative_activities"]) == 1
    assert len(parsed.sections["behavioral_notes"]) == 1
    assert len(parsed.sections["attendance"]) >= 1


def test_rule_engine_masks_and_filters():
    parsed = parse_record_file(FIXTURES / "record_b.txt")
    engine = RuleEngine.from_files(DOCS / "exclusion_rules.yaml", DOCS / "grade2_mode.yaml")
    payload = engine.apply(parsed.sections)

    creative_texts = [x["text"] for x in payload["sections"]["creative_activities"]]
    assert all("진로희망" not in t for t in creative_texts)


def test_golden_outputs():
    for fixture in ["record_a", "record_b", "record_c"]:
        actual = _run_pipeline(FIXTURES / f"{fixture}.txt")
        expected = (GOLDEN / f"{fixture}.md").read_text(encoding="utf-8")
        assert actual == expected
