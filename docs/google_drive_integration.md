# Google Drive 참고자료 업로드/연동 가이드

## 1) 업로드
1. 생활기록부 원문(PDF/TXT)을 Google Drive에 업로드
2. 파일 공유 설정을 "링크가 있는 사용자(뷰어)"로 변경
3. 공유 링크 복사

예시 링크
- `https://drive.google.com/file/d/<FILE_ID>/view?usp=sharing`
- `https://drive.google.com/open?id=<FILE_ID>`

## 2) 연동 방식
분석기는 Google Drive URL을 입력으로 받아 파일 ID를 추출한 뒤, 다운로드 URL(`uc?export=download&id=...`)로 파일을 받아 파싱한다.

## 3) 사용 예시 (Python)
```python
from school_record_analyzer import parse_record_file

parsed = parse_record_file("https://drive.google.com/file/d/<FILE_ID>/view?usp=sharing")
print(parsed.sections.keys())
```

## 4) 운영 시 주의
- 개인정보 포함 문서는 접근권한을 최소화하고, 만료 링크/전용 폴더 권한을 권장.
- 보고서 출력은 반드시 마스킹/제외 규칙(`exclusion_rules.yaml`)을 통과시킬 것.
- 대용량 파일은 사전 텍스트 변환(TXT) 후 분석을 권장.
