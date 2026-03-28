# 생활기록부 분석기 (School Record Analyzer)

고2 학생의 생활기록부를 **1학년 기록 중심**으로 분석하고, 근거가 포함된 Markdown 보고서를 생성하는 프로젝트입니다.

## 1. 핵심 기능
- PDF/TXT 또는 Google Drive 공유 링크 입력
- 섹션 파싱: 교과성적, 세특, 창체, 행특, 출결
- 규칙 엔진 적용
  - 개인정보 마스킹
  - 수상/자격증/진로희망 등 핵심 평가 근거 제외
  - 고2 모드(1학년 기록 중심) 필터
- 템플릿 기반 근거 포함 보고서 생성
- Streamlit Pages 기반 UI 실행 지원

---

## 2. 프로젝트 구조
```text
.
├── app.py                          # Streamlit 메인 홈
├── pages/
│   ├── 1_Record_Analyzer.py        # 분석 실행 페이지
│   └── 2_Rule_Preview.py           # 규칙 적용 결과 점검 페이지
├── src/school_record_analyzer/
│   ├── parser.py                   # PDF/TXT/Drive 입력 파싱
│   ├── rules.py                    # exclusion + grade2 규칙 엔진
│   ├── renderer.py                 # 보고서 렌더러
│   └── drive.py                    # Google Drive 링크 처리
├── docs/
│   ├── report_template.md
│   ├── exclusion_rules.yaml
│   ├── grade2_mode.yaml
│   ├── student_record.schema.json
│   └── google_drive_integration.md
└── tests/
    ├── fixtures/
    ├── golden/
    ├── test_pipeline.py
    └── test_drive.py
```

---

## 3. 설치 및 실행

### 3-1) 로컬 실행 환경 준비
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install streamlit pytest
```

> PDF 입력을 사용하려면 `pypdf`를 추가 설치하세요.
```bash
pip install pypdf
```

### 3-2) Pages UI 실행
```bash
streamlit run app.py
```

실행 후 브라우저에서:
- **Record Analyzer**: 파일 업로드/경로/Drive 링크로 보고서 생성
- **Rule Preview**: 텍스트 입력 후 규칙 적용 결과 확인

---

## 4. 코드 기반 사용 예시
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

Google Drive 링크 예시:
```python
parsed = parse_record_file("https://drive.google.com/file/d/<FILE_ID>/view?usp=sharing")
```

---

## 5. 테스트
```bash
PYTHONPATH=src pytest -q
```

- `test_pipeline.py`: 파싱/규칙/골든 출력 검증
- `test_drive.py`: Drive 링크 처리 로직 검증

---

## 6. 운영 가이드
- 개인정보가 포함된 원문은 최소 권한으로 접근 관리하세요.
- 보고서 결과는 반드시 규칙 엔진 통과 후 사용하세요.
- 분석 품질은 점수화보다 **원문 근거의 정확성/추적성**을 우선하세요.

