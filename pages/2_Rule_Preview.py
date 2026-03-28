from __future__ import annotations

from pathlib import Path
import tempfile

import streamlit as st

from school_record_analyzer.parser import parse_record_file
from school_record_analyzer.rules import RuleEngine

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

st.title("🧪 Rule Preview")
st.caption("텍스트를 임시 파일로 파싱한 뒤 exclusion/grade2 규칙이 적용된 결과를 확인합니다.")

default_text = """교과성적
1학년 1학기 국어 성취도 A
세특
1학년 발표 수업에서 논리적 전개
창체
1학년 진로희망 발표
행특
1학년 협력 태도 우수
출결
1학년 결석 0
"""

text = st.text_area("생활기록부 텍스트 입력", value=default_text, height=260)

if st.button("규칙 적용 보기"):
    temp = Path(tempfile.gettempdir()) / "rule_preview_input.txt"
    temp.write_text(text, encoding="utf-8")

    parsed = parse_record_file(temp)
    engine = RuleEngine.from_files(DOCS / "exclusion_rules.yaml", DOCS / "grade2_mode.yaml")
    payload = engine.apply(parsed.sections)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Parsed Sections")
        st.json(parsed.sections)
    with col2:
        st.subheader("After Rules")
        st.json(payload)
