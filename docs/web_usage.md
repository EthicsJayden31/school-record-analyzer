# 웹 기반 사용 가이드

이 프로젝트는 **터미널에서 분석 명령을 직접 입력하는 방식이 아니라, 웹 화면(Streamlit)에서 업로드/클릭으로 사용하는 방식**을 기본으로 제공합니다.

## 1) 로컬 웹으로 실행

아래 중 하나로 실행하면 브라우저에서 사용 가능합니다.

- `./run_app.sh`
- `streamlit run app.py`

실행 후 접속 주소 예시: `http://localhost:8501`

## 2) 웹 화면에서만 사용하는 순서

1. `생활기록부 파일 업로드 (PDF/TXT)`에 파일 업로드
2. `분석 실행` 버튼 클릭
3. 결과 보고서 확인
4. `보고서 다운로드 (.md)` 클릭

## 3) 완전한 원격 웹(배포)로 사용

학교/학원 내부에서 링크로 접속만 하도록 하려면 Streamlit Community Cloud 또는 사내 서버에 배포하면 됩니다.

### Streamlit Community Cloud 빠른 절차

1. GitHub에 저장소 푸시
2. https://share.streamlit.io 접속
3. New app 생성
4. Main file path: `app.py`
5. Deploy

배포 후에는 사용자가 Python/터미널 없이 URL로 바로 접속해 사용할 수 있습니다.
