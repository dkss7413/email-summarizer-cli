# AI 기반 이메일/메시지 요약 CLI 도구

## 📋 소개
긴 이메일, 메신저 대화, 문서 텍스트 등을 자연어 요약하여 핵심 정보를 빠르게 파악할 수 있도록 돕는 커맨드라인 도구(CLI)입니다.

## 🚀 개발 진행 상황

### ✅ 1단계: Typer 기반 CLI 뼈대 구현 및 옵션 파싱
- [x] Typer CLI 앱 구조 설정
- [x] 옵션 파싱 (`--input`, `--length`, `--language`, `--highlight`, `--verbose`)

### ✅ 2단계: 입력(파일/표준입력) 처리 로직 구현
- [x] 파일 입력 처리 (다중 인코딩 지원: UTF-8, CP949, EUC-KR)
- [x] 텍스트 검증 (길이, 내용 유효성)
- [x] 오류 처리 및 사용자 피드백
- [x] 상세 정보 출력 (`--verbose` 옵션)

### ✅ 3단계: 간단한 요약 알고리즘으로 MVP 동작 확인
- [x] 문장 추출 기반 요약 로직
- [x] 기본 출력 포맷 구현
- [x] MVP 동작 테스트

### ✅ 4단계: TF-IDF 기반 키워드 추출 및 강조 기능 추가
- [x] TF-IDF 알고리즘 구현 (단어 빈도 × 역문서빈도)
- [x] 향상된 키워드 강조 (중요도별 색상 구분, 중복/중첩 방지)
- [x] 중요도 기반 정렬 및 점수 표시
- [x] 개선된 문장 중요도 분석 (위치, 길이, 패턴 매칭)
- [x] CLI 구조 개선 (직관적인 명령어)

### ✅ 5단계: 다국어 지원 및 고급 기능
- [x] 한글/영어/혼합 텍스트 자동 감지 및 처리
- [x] 영어/혼합 키워드 강조(복수형, 대소문자, 중첩 방지)
- [x] 언어별 불용어/패턴/길이 최적화
- [x] 샘플 파일(영어, 혼합) 추가 및 테스트

### ⏳ 6단계: AI 모델 기반 고급 기능 및 웹 API
- [x] **Sentence Transformers 기반 임베딩 모델 적용**
- [x] **MMR (Maximal Marginal Relevance) 알고리즘으로 요약 품질 향상**
- [x] **감정 분석 기능 추가 (BERT 기반 다국어 모델)**
- [x] **문장 유사도 기반 클러스터링 요약**
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
python -m email_summarizer sample/sample.txt
```

## 📖 사용법 및 CLI 옵션

### 기본 사용법
```bash
# 파일에서 텍스트 요약 (언어 자동 감지)
python -m email_summarizer --file sample/sample.txt

# 상세 정보와 함께 요약
python -m email_summarizer --file sample/sample.txt --verbose

# 긴 요약
python -m email_summarizer --file sample/sample.txt --length long

# 키워드 강조 (색상 및 굵기)
python -m email_summarizer --file sample/sample.txt --highlight

# 영어/혼합 텍스트 요약 (자동 감지)
python -m email_summarizer --file sample/sample_english.txt --highlight
python -m email_summarizer --file sample/sample_mixed.txt --highlight

# 표준 입력에서 텍스트 요약 (파이프 지원)
echo "요약할 텍스트" | python -m email_summarizer --highlight
```

### 지원 옵션
| 옵션 | 축약 | 설명 | 기본값 |
|------|------|------|--------|
| `--file` | `-f` | 요약할 텍스트 파일 경로 | None (표준 입력) |
| `--length` | `-l` | 요약 길이: `short`, `normal`, `long` | `normal` |
| `--highlight` | - | 키워드 강조 출력 (색상 및 굵기) | `True` |
| `--no-highlight` | - | 키워드 강조 비활성화 | - |

## 🏗️ 프로젝트 구조
```
email-summarizer-cli/
├── email_summarizer/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
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
- **Sentence Transformers**: 다국어 임베딩 모델 (`paraphrase-multilingual-MiniLM-L12-v2`)
- **Transformers**: BERT 기반 감정 분석 모델 (`nlptown/bert-base-multilingual-uncased-sentiment`)
- **Scikit-learn**: 코사인 유사도, 클러스터링
- **NumPy**: 수치 계산 및 배열 처리
- **TF-IDF**: 키워드 추출 알고리즘
- **MMR (Maximal Marginal Relevance)**: 핵심성과 다양성을 고려한 요약 알고리즘
- **정규표현식**: 텍스트/문장 처리
- **다국어 지원**: 한글/영어/혼합 자동 감지 및 최적화
- **불용어/패턴/길이**: 언어별 최적화
- **중복/중첩 없는 키워드 강조**

## 🧪 테스트 및 샘플 파일
```bash
# 한글 샘플
python -m email_summarizer --file sample/sample.txt --highlight --verbose

# 영어 샘플
python -m email_summarizer --file sample/sample_english.txt --highlight --verbose

# 혼합 샘플
python -m email_summarizer --file sample/sample_mixed.txt --highlight --verbose
```

### 출력 예시 (AI 모델 기반 요약 및 감정 분석)
```
📝 요약 결과:

이 문서는 AI-powered text summarization system의 다국어 지원 기능에 대해 설명합니다. The system automatically detects the language of input text using character pattern analysis. 각 언어별로 최적화된 처리를 제공합니다.

🔑 주요 키워드:
  1. system (TF-IDF: 0.085)
  2. 언어 (TF-IDF: 0.082)
  3. detection (TF-IDF: 0.078)
  4. processing (TF-IDF: 0.075)
  5. 기능 (TF-IDF: 0.072)

🌐 언어 감지: Mixed
😊 감정 분석: 4 stars (신뢰도: 0.85)

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