# AI 기반 이메일/메시지 요약 CLI 도구

## 📋 소개
긴 이메일, 메신저 대화, 문서 텍스트 등을 자연어 요약하여 핵심 정보를 빠르게 파악할 수 있도록 돕는 커맨드라인 도구(CLI)입니다.

## 🚀 개발 진행 상황

### ✅ 1단계: Typer 기반 CLI 뼈대 구현 및 옵션 파싱
- [x] Typer CLI 앱 구조 설정
- [x] 옵션 파싱 (`--input`, `--length`, `--language`, `--highlight`, `--verbose`)

### ✅ 2단계: 입력(파일/표준입력) 처리 로직 구현
- [x] 파일 입력 처리 (다중 인코딩 지원: UTF-8, CP949, EUC-KR)
- [x] 오류 처리
- [x] 상세 정보 출력 (`--verbose` 옵션)

### ✅ 3단계: 간단한 요약 알고리즘으로 MVP 동작 확인
- [x] 문장 추출 기반 요약 로직
- [x] 기본 출력 포맷 구현

### ✅ 4단계: TF-IDF 기반 키워드 추출 및 강조 기능 추가
- [x] TF-IDF 알고리즘 구현 (단어 빈도 × 역문서빈도)
- [x] 향상된 키워드 강조 (중요도별 색상 구분, 중복/중첩 방지)
- [x] CLI 구조 개선 (직관적인 명령어)

### ✅ 5단계: 다국어 지원 및 고급 기능
- [x] 한글/영어/혼합 텍스트 자동 감지 및 처리
- [x] 영어/혼합 키워드 강조(복수형, 대소문자, 중첩 방지)

### ✅ 6단계: 요약 알고리즘 고도화 및 기능 추가
- [x] 요약 모델 고도화 (Sentence Transformers → BART/KoBART)  
  • 초기에는 Sentence Transformers 기반 추출 요약을 적용했으나,  
  • 이후 문맥 이해 기반의 생성형 모델로 BART/KoBART를 도입하여 요약 품질을 향상시켰습니다.
- [x] 감정 분석 기능 추가 (BERT 기반 다국어 모델)
- [x] 성능 최적화 및 안정성 개선

### ⏳ 7단계: 사용자 인터페이스 고도화 (GUI + Gmail API)
- [x] Tkinter 기반 데스크톱 GUI 인터페이스 구현
- [x] Gmail API 연동 기능 추가
- [ ] 성능 최적화 및 안정성 개선

## 🛠️ 설치 및 실행

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd email-summarizer-cli
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 실행
```bash
# 도움말 보기
python -m email_summarizer --help

# 파일에서 요약
python -m email_summarizer summarize --file sample/sample.txt

# GUI 실행
python -m email_summarizer gui
```

## 📖 CLI 사용법 및 옵션

### 기본 사용법
```bash
# 파일에서 텍스트 요약 (언어 자동 감지)
python -m email_summarizer summarize --file sample/sample.txt

# Gmail에서 최근 메일 요약
python -m email_summarizer gmail

# 키워드 강조 (색상 및 굵기)
python -m email_summarizer summarize --file sample/sample.txt --highlight

# 키워드 강조 비활성화
python -m email_summarizer summarize --file sample/sample.txt --no-highlight

# 영어/혼합 텍스트 요약 (자동 감지)
python -m email_summarizer summarize --file sample/sample_english.txt --highlight
python -m email_summarizer summarize --file sample/sample_mixed.txt --highlight

# 표준 입력에서 텍스트 요약 (파이프 지원)
echo "요약할 텍스트" | python -m email_summarizer summarize --highlight

# GUI 실행
python -m email_summarizer gui
```

### 🔑 credentials.json 생성 및 위치 안내

- Gmail 등 Google API 연동을 위해서는 `credentials.json` 파일이 필요합니다.
- [Google Cloud Console](https://console.cloud.google.com/)에서 OAuth 2.0 클라이언트 ID를 생성하고, 다운로드한 `credentials.json` 파일을 프로젝트 루트(최상위 폴더)에 위치시켜 주세요.
- 예시 경로:
  ```
  email-summarizer-cli/
  ├── credentials.json  # ← 여기에 위치
  ├── email_summarizer/
  ├── sample/
  └── ...
  ```
- 이 파일은 개인정보를 포함하므로 `.gitignore`에 반드시 추가해야 하며, 외부에 공유하지 않도록 주의하세요.

### 지원 옵션
| 옵션 | 축약 | 설명 | 기본값 |
|------|------|------|--------|
| `--file` | `-f` | 요약할 텍스트 파일 경로 | None (표준 입력) |
| `--highlight` | - | 키워드 강조 출력 (색상 및 굵기) | `True` |
| `--no-highlight` | - | 키워드 강조 비활성화 | - |
| `--length` | - | 요약 길이 조절 (short: 짧게, long: 길게, auto: 자동) | auto |

## 🖥️ GUI 사용법

### 실행
```bash
python -m email_summarizer gui
```

### 주요 기능
1. 📁 파일 업로드
2. 📧 Gmail 연동 (최근 10개 이메일 불러오기/요약)
3. ✏️ 직접 입력
4. ⚙️ 요약 길이 조절(짧게/길게/자동), 키워드 강조 등 설정
5. 📊 실시간 진행(프로그레스바)
6. 📋 결과 스크롤 출력

### 화면 구성
- 상단: 제목/입력방식 버튼
- 중앙: 텍스트 입력
- 하단: 결과 출력

## 🏗️ 프로젝트 구조
```
email-summarizer-cli/
├── email_summarizer/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── gui.py              # GUI 인터페이스
│   ├── gmail_utils.py      # Gmail API 연동
│   ├── utils.py
│   └── summarizer.py
├── sample/
│   ├── sample.txt           # 기본 샘플
│   ├── sample_email.txt     # 이메일 형태 샘플
│   ├── sample_article.txt   # 기술 문서 샘플
│   ├── sample_english.txt   # 영어 기술 문서 샘플
│   └── sample_mixed.txt     # 한영 혼합 샘플
├── tests/
│   └── test_summarizer.py
├── requirements.txt
├── setup.py
└── README.md
```

## 🔧 기술 스택 및 특징
- **Python 3.7+**
- **Typer**: CLI 프레임워크
- **Tkinter**: GUI 프레임워크 (Python 표준 라이브러리)
- **Transformers**: BERT 기반 감정 분석 모델 (`nlptown/bert-base-multilingual-uncased-sentiment`)
- **Scikit-learn**: 코사인 유사도, 클러스터링
- **NumPy**: 수치 계산 및 배열 처리
- **TF-IDF**: 키워드 추출 알고리즘
- **MMR (Maximal Marginal Relevance)**: 핵심성과 다양성을 고려한 요약 알고리즘
- **정규표현식**: 텍스트/문장 처리
- **다국어 지원**: 한글/영어/혼합 자동 감지 및 최적화
- **불용어/패턴/길이**: 언어별 최적화
- **중복/중첩 없는 키워드 강조**
- **seq2seq 기반(BART/KoBART) 요약 모델로 교체**
- **멀티스레딩**: GUI에서 백그라운드 처리 지원

## 🧪 테스트 및 샘플 파일

### 📊 샘플 데이터 출처 및 생성 방식
본 프로젝트의 `sample/` 디렉토리에 포함된 모든 샘플 파일들은 **생성형 AI를 통해 생성된 테스트용 데이터**입니다.

#### 생성 목적
- 이메일 요약 기능 테스트
- 메신저 대화 요약 기능 테스트  
- 다양한 언어(한국어, 영어, 혼합) 및 텍스트 유형별 요약 품질 검증
- CLI 및 GUI 인터페이스 동작 확인

#### 데이터 유형별 설명
- `sample_email_*.txt`: 이메일 형태의 가상 대화/문서
- `sample_article_*.txt`: 기술 문서 및 뉴스 기사 형태
- `sample_mixed.txt`: 한국어와 영어가 혼합된 텍스트
- `sample_english.txt`: 영어로 작성된 기술 문서
- `sample.txt`: 기본 한국어 텍스트

#### 주의사항
- 모든 샘플 데이터는 실제 개인정보나 민감한 내용을 포함하지 않습니다
- 테스트 목적으로만 사용되며, 실제 서비스에서는 사용자 입력 텍스트를 사용합니다

### 출력 예시 (AI 모델 기반 요약 및 감정 분석)
```
📝 요약 결과:

이 문서는 AI-powered text summarization system의 다국어 지원 기능에 대해 설명합니다. The system automatically detects the language of input text using character pattern analysis. 각 언어별로 최적화된 처리를 제공합니다.

🌐 언어 감지: Mixed
😊 감정 분석: 중립적 (신뢰도: 보통)

📊 통계:
  • 원본 길이: 2,450자
  • 요약 길이: 156자
  • 문장 수: 15개 → 3개
```

## 🤝 기여하기
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의
프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 생성해 주세요.
