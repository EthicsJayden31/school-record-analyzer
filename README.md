# 생활기록부 분석기 (School Record Analyzer)

고2 학생의 생활기록부를 **1학년 기록 중심**으로 분석하고, 근거가 포함된 Markdown 보고서를 생성합니다.

## 빠른 시작 (처음 사용자용)

### 0) 준비
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install streamlit pytest
```

> PDF 입력까지 사용하려면:
```bash
pip install pypdf
```

### 1) 실행 (아래 둘 중 하나)
```bash
./run_app.sh
```
또는
```bash
streamlit run app.py
```

### 2) 브라우저에서 바로 분석
앱 첫 화면(`app.py`)에 이미 **분석 실행 탭**이 있으므로, pages를 이동하지 않아도 됩니다.

1. PDF/TXT 업로드 또는 Drive 링크 입력
2. `분석 실행` 클릭
3. 생성된 보고서 확인 후 `보고서 다운로드 (.md)` 클릭

---

## 프로젝트 개요
- 입력: PDF/TXT 로컬 파일, Google Drive 공유 링크
- 출력: 근거 포함 Markdown 보고서
- 분석 축: 학업역량/진로역량/공동체역량(필요 시 4축)
- 규칙: 마스킹, 제외 키워드 필터, 1학년 기록 중심 필터

---

## 폴더 구조
```text
.
├── app.py                          # 첫 화면에서 바로 분석 가능한 메인 앱
├── run_app.sh                      # 원클릭 실행 스크립트
├── pages/
│   ├── 1_Record_Analyzer.py        # 분석 전용 페이지
│   └── 2_Rule_Preview.py           # 규칙 확인 페이지
├── src/school_record_analyzer/
│   ├── parser.py
│   ├── rules.py
│   ├── renderer.py
│   └── drive.py
├── docs/
└── tests/
```

---

## 코드로 직접 사용하는 방법
```python
from school_record_analyzer.parser import parse_record_file
from school_record_analyzer.rules import RuleEngine
from school_record_analyzer.renderer import render_report

parsed = parse_record_file("tests/fixtures/record_a.txt")
engine = RuleEngine.from_files("docs/exclusion_rules.yaml", "docs/grade2_mode.yaml")
payload = engine.apply(parsed.sections)
report = render_report(payload, "docs/report_template.md")
print(report)
```

Google Drive 링크 입력 예시:
```python
parsed = parse_record_file("https://drive.google.com/file/d/<FILE_ID>/view?usp=sharing")
```

---

## 테스트
```bash
PYTHONPATH=src pytest -q
```

- `tests/test_pipeline.py`: 파서/규칙/골든 출력 검증
- `tests/test_drive.py`: Drive 링크 처리 검증

---

## 문제 해결
- `streamlit: command not found`
  - `pip install streamlit` 실행 후 재시도
- PDF 입력에서 오류 발생
  - `pip install pypdf` 설치 여부 확인
- 권한 문제로 Drive 다운로드 실패
  - 공유 설정이 "링크가 있는 사용자(뷰어)"인지 확인
