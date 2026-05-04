# 생활기록부 분석기 (완전 초보용 안내서)

이 문서는 **코딩을 전혀 모르는 사람**도 설치부터 실행까지 따라할 수 있게 작성했습니다.

---

## 0. 이 프로그램이 하는 일
이 프로그램은 생활기록부(PDF/TXT)를 읽어서,
- 교과성적
- 세특
- 창체
- 행특
- 출결
을 나누고, 규칙을 적용한 뒤, **근거가 포함된 분석 보고서(.md)**를 만들어 줍니다.

---

## 1. 준비물 (딱 2개)
1) 컴퓨터 (Windows / macOS)
2) 인터넷

그리고 아래 2개를 설치해야 합니다.
- Python 3.11 이상
- 터미널(명령어 창)

---

## 2. Python 설치 (처음 한 번만)

### Windows
1. 웹 브라우저에서 `python.org` 접속
2. Downloads → Python 3.11 이상 설치 파일 다운로드
3. 설치할 때 **반드시** `Add Python to PATH` 체크
4. Install Now 클릭

### macOS
1. 웹 브라우저에서 `python.org` 접속
2. macOS용 Python 3.11 이상 설치
3. 설치 완료

설치 확인:
```bash
python --version
```
또는
```bash
python3 --version
```

`Python 3.11.x` 같이 보이면 성공입니다.

---

## 3. 프로젝트 폴더 열기

1. 이 저장소(프로젝트)를 다운로드(또는 git clone)
2. 압축을 풀거나 폴더를 준비
3. 터미널에서 해당 폴더로 이동

예시:
```bash
cd /path/to/school-record-analyzer
```

Windows 예시:
```bash
cd C:\Users\내이름\Downloads\school-record-analyzer
```

---

## 4. 설치 (복붙용 명령어)

아래 명령어를 **한 줄씩 그대로 복사해서 실행**하세요.

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install streamlit pytest pypdf
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
pip install streamlit pytest pypdf
```

> 만약 실행 정책 오류가 나오면(Windows), PowerShell을 관리자 권한으로 열고:
> `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
> 한 번 실행한 뒤 다시 시도하세요.

---

## 5. 프로그램 실행 (아주 쉬운 방법)

### 방법 A (권장)
```bash
./run_app.sh
```

### 방법 B
```bash
streamlit run app.py
```

실행하면 브라우저가 자동으로 열리거나, 터미널에 주소가 나옵니다.
보통 `http://localhost:8501` 입니다.

---

## 6. 화면에서 실제로 사용하는 순서

앱을 열면 첫 화면에서 바로 사용할 수 있습니다.

1. **[🚀 분석 실행] 탭** 클릭 (기본으로 열림)
2. 아래 둘 중 하나 선택
   - `생활기록부 파일 업로드 (PDF/TXT)`
   - `로컬 경로/Google Drive 링크 입력`
3. `분석 실행` 버튼 클릭
4. 결과 보고서가 화면에 나타남
5. `보고서 다운로드 (.md)` 버튼으로 저장

추가 확인이 필요하면
- **[🧪 규칙 미리보기] 탭**에서 텍스트를 넣고 규칙 적용 결과(JSON)를 볼 수 있습니다.

---

## 7. Google Drive 링크 사용 방법

1. Drive에 파일 업로드
2. 공유 설정을 `링크가 있는 사용자(뷰어)`로 변경
3. 공유 링크 복사
4. 앱의 링크 입력 칸에 붙여넣기

예시 링크:
- `https://drive.google.com/file/d/<FILE_ID>/view?usp=sharing`
- `https://drive.google.com/open?id=<FILE_ID>`

---

## 8. 자주 발생하는 문제 해결

### Q1. `streamlit: command not found`
A. 가상환경 활성화 후 아래 실행:
```bash
pip install streamlit
```

### Q2. PDF 파일에서 오류
A. 아래 설치:
```bash
pip install pypdf
```

### Q3. Drive 링크가 안 읽힘
A. 파일 공유 권한이 "링크가 있는 사용자(뷰어)"인지 확인하세요.

### Q4. 명령어가 너무 어렵다
A. 아래 순서만 기억하세요.
1) 가상환경 만들기
2) 패키지 설치
3) `streamlit run app.py`

---

## 9. 테스트(선택)
프로그램이 정상인지 확인하려면:
```bash
PYTHONPATH=src pytest -q
```

---

## 10. 한 줄 요약
**설치 후 `streamlit run app.py`만 실행하면, 브라우저에서 파일 업로드 → 분석 → 보고서 다운로드까지 할 수 있습니다.**

---

## 11. 웹 기반으로만 사용하고 싶다면

이 프로젝트는 이미 **웹 UI(Streamlit)** 로 동작합니다.

- 로컬 실행: `./run_app.sh` 또는 `streamlit run app.py`
- 완전 웹 배포(사용자는 터미널/파이썬 불필요): `docs/web_usage.md` 참고

즉, 분석 자체는 브라우저 화면에서 업로드/버튼 클릭만으로 진행할 수 있습니다.
