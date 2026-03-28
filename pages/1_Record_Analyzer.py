from __future__ import annotations

from pathlib import Path
import tempfile

import streamlit as st

from school_record_analyzer.parser import parse_record_file
from school_record_analyzer.renderer import render_report
from school_record_analyzer.rules import RuleEngine

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


st.title("🧾 Record Analyzer")

st.caption("PDF/TXT 파일 또는 Google Drive 공유 링크를 입력해 보고서를 생성합니다.")

uploaded = st.file_uploader("생활기록부 파일 업로드 (PDF/TXT)", type=["pdf", "txt"])
source_text = st.text_input("또는 로컬 경로/Google Drive 링크 입력")

if st.button("분석 실행", type="primary"):
    source: str | Path

    if uploaded is not None:
        suffix = "." + uploaded.name.split(".")[-1].lower()
        temp_path = Path(tempfile.gettempdir()) / f"uploaded_record{suffix}"
        temp_path.write_bytes(uploaded.getvalue())
        source = temp_path
    elif source_text.strip():
        source = source_text.strip()
    else:
        st.error("파일 업로드 또는 입력값 중 하나를 제공해 주세요.")
        st.stop()

    try:
        parsed = parse_record_file(source)
        engine = RuleEngine.from_files(DOCS / "exclusion_rules.yaml", DOCS / "grade2_mode.yaml")
        payload = engine.apply(parsed.sections)
        report = render_report(payload, DOCS / "report_template.md")
    except Exception as exc:
        st.exception(exc)
        st.stop()

    st.success("분석이 완료되었습니다.")
    st.subheader("생성된 보고서")
    st.markdown(report)

    st.download_button(
        "보고서 다운로드 (.md)",
        data=report.encode("utf-8"),
        file_name="analysis_report.md",
        mime="text/markdown",
    )

    with st.expander("파싱 섹션 미리보기"):
        st.json(parsed.sections)
