from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="생활기록부 분석기", page_icon="📘", layout="wide")

st.title("📘 생활기록부 분석기")
st.markdown(
    """
고2 학생의 생활기록부를 **1학년 기록 중심**으로 분석하는 도구입니다.

왼쪽 사이드바의 Pages에서 다음 기능을 사용할 수 있습니다.
- **Record Analyzer**: 파일/경로/Google Drive 링크 입력 후 보고서 생성
- **Rule Preview**: 규칙 적용 결과(JSON) 점검

> 본 도구는 점수화보다 **근거 추출**과 **판독 근거**를 우선합니다.
"""
)

st.info("실행 예시: `streamlit run app.py`")
