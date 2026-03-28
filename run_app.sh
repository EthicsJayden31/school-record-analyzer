#!/usr/bin/env bash
set -euo pipefail

if ! command -v streamlit >/dev/null 2>&1; then
  echo "[안내] streamlit이 설치되어 있지 않습니다."
  echo "다음 명령을 먼저 실행하세요: pip install streamlit"
  exit 1
fi

streamlit run app.py
