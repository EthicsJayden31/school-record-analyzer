from __future__ import annotations

from pathlib import Path
import tempfile

import streamlit as st

from school_record_analyzer.parser import parse_record_file
from school_record_analyzer.renderer import render_report
from school_record_analyzer.rules import RuleEngine

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"

st.set_page_config(page_title="생활기록부 분석기", page_icon="📘", layout="wide")

st.title("📘 생활기록부 분석기")
st.markdown("""
처음 접속한 화면에서 **바로 분석 실행**이 가능하도록 구성했습니다.
왼쪽 Pages로 이동하지 않아도 아래 탭에서 바로 사용할 수 있습니다.
""")

with st.expander("처음 사용자용 3단계 실행 가이드", expanded=True):
    st.markdown(
        """
1. 아래 **분석 실행 탭**에서 PDF/TXT 파일을 업로드하거나 Google Drive 링크를 입력합니다.
2. **분석 실행** 버튼을 누릅니다.
3. 화면의 Markdown 보고서를 확인하고 `보고서 다운로드` 버튼으로 저장합니다.

> 터미널 실행 명령: `streamlit run app.py`
"""
    )

tab_analyze, tab_preview = st.tabs(["🚀 분석 실행", "🧪 규칙 미리보기"])

with tab_analyze:
    st.subheader("생활기록부 보고서 생성")
    uploaded = st.file_uploader("생활기록부 파일 업로드 (PDF/TXT)", type=["pdf", "txt"], key="home_upload")
    source_text = st.text_input("또는 로컬 경로/Google Drive 링크 입력", key="home_source")

    if st.button("분석 실행", type="primary", key="home_run"):
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
        st.markdown(report)
        st.download_button(
            "보고서 다운로드 (.md)",
            data=report.encode("utf-8"),
            file_name="analysis_report.md",
            mime="text/markdown",
            key="home_download",
        )

        with st.expander("파싱 섹션 미리보기"):
            st.json(parsed.sections)

with tab_preview:
    st.subheader("규칙 적용 결과 미리보기")
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
    text = st.text_area("생활기록부 텍스트 입력", value=default_text, height=220, key="home_preview_text")

    if st.button("규칙 적용 보기", key="home_preview_btn"):
        temp = Path(tempfile.gettempdir()) / "rule_preview_input.txt"
        temp.write_text(text, encoding="utf-8")

        parsed = parse_record_file(temp)
        engine = RuleEngine.from_files(DOCS / "exclusion_rules.yaml", DOCS / "grade2_mode.yaml")
        payload = engine.apply(parsed.sections)

        c1, c2 = st.columns(2)
        with c1:
            st.write("Parsed")
            st.json(parsed.sections)
        with c2:
            st.write("After Rules")
            st.json(payload)
