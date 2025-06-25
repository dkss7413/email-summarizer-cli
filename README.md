# AI 기반 이메일/메시지 요약 CLI 도구

## 📋 소개
긴 이메일, 메신저 대화, 문서 텍스트 등을 자연어 요약하여 핵심 정보를 빠르게 파악할 수 있도록 돕는 커맨드라인 도구(CLI)입니다.

## 🚀 개발 진행 상황

### ✅ 1단계: Typer 기반 CLI 뼈대 구현 및 옵션 파싱
- [x] Typer CLI 앱 구조 설정
- [x] 서브커맨드 구조 (`summarize`)
- [x] 옵션 파싱 (`--input`, `--length`, `--language`, `--highlight`, `--verbose`)
- [x] 도움말 시스템 구현

### ✅ 2단계: 입력(파일/표준입력) 처리 로직 구현
- [x] 파일 입력 처리 (다중 인코딩 지원: UTF-8, CP949, EUC-KR)
- [x] 표준입력 처리 (파이프 지원, Windows 인코딩 이슈 있음)
- [x] 텍스트 검증 (길이, 내용 유효성)
- [x] 오류 처리 및 사용자 피드백
- [x] 상세 정보 출력 (`--verbose` 옵션)

### ✅ 3단계: 간단한 요약 알고리즘으로 MVP 동작 확인
- [x] 문장 추출 기반 요약 로직
- [x] 기본 출력 포맷 구현
- [x] MVP 동작 테스트

### 🔄 4단계: 키워드 추출 및 강조 기능 추가 (진행 예정)
- [ ] 키워드 추출 알고리즘 개선
- [ ] 키워드 강조 출력 개선
- [ ] 중요도 기반 정렬

### ⏳ 5단계: 예외/오류 처리 및 도움말 강화
- [ ] 상세한 오류 메시지
- [ ] 사용 예시 추가
- [ ] 도움말 개선

### ⏳ 6단계: 테스트 코드 작성
- [ ] 단위 테스트
- [ ] 통합 테스트
- [ ] 테스트 커버리지

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

# summarize 커맨드 도움말
python -m email_summarizer summarize --help
```

## 📖 현재 사용법

### 기본 사용법
```bash
# 파일에서 텍스트 요약
python -m email_summarizer summarize --input sample/sample.txt

# 상세 정보와 함께 요약
python -m email_summarizer summarize --input sample/sample.txt --verbose

# 긴 요약
python -m email_summarizer summarize --input sample/sample.txt --length long

# 키워드 강조
python -m email_summarizer summarize --input sample/sample.txt --highlight

# 모든 옵션 조합
python -m email_summarizer summarize --input sample/sample.txt --length long --highlight --verbose
```

### 현재 지원하는 옵션
| 옵션 | 축약 | 설명 | 기본값 |
|------|------|------|--------|
| `--input` | `-i` | 입력 파일 경로 (생략 시 표준입력) | None |
| `--length` | `-l` | 요약 길이: `short` 또는 `long` | `short` |
| `--language` | `-lang` | 요약 언어: `ko` 또는 `en` | `ko` |
| `--highlight` | `-hl` | 키워드 강조 출력 여부 | `False` |
| `--verbose` | `-v` | 상세 정보 출력 | `False` |

## 🏗️ 프로젝트 구조
```
email-summarizer-cli/
├── email_summarizer/
│   ├── __init__.py          # 패키지 초기화
│   ├── __main__.py          # 모듈 실행 엔트리포인트
│   ├── cli.py              # Typer CLI 구현 ✅
│   ├── utils.py            # 입력 처리 및 유틸리티 함수 ✅
│   └── summarizer.py       # 요약 로직 ✅
├── sample/                 # 샘플 파일들
│   ├── sample.txt          # 기본 테스트용 샘플 파일
│   ├── sample_email.txt    # 이메일 형태 샘플 파일
│   └── sample_article.txt  # 기술 문서 형태 샘플 파일
├── tests/
│   └── test_summarizer.py  # 테스트 코드 (작성 예정) ⏳
├── requirements.txt        # 의존성 목록
├── setup.py               # 패키지 설정
└── README.md              # 프로젝트 문서
```

## 🔧 기술 스택
- **Python 3.7+** - 메인 프로그래밍 언어
- **Typer** - CLI 프레임워크
- **Click** - Typer의 기반 라이브러리
- **Rich** - 터미널 출력 포맷팅

## 🧪 현재 테스트 가능한 기능

### 다양한 텍스트 요약 테스트
```bash
# 기본 샘플 텍스트
python -m email_summarizer summarize --input sample/sample.txt --verbose

# 이메일 형태 텍스트
python -m email_summarizer summarize --input sample/sample_email.txt --verbose

# 기술 문서 형태 텍스트
python -m email_summarizer summarize --input sample/sample_article.txt --verbose

# 오류 처리 테스트
python -m email_summarizer summarize --input nonexistent.txt

# 빈 파일 테스트
echo "" > empty.txt
python -m email_summarizer summarize --input empty.txt
```

### 현재 출력 예시
```
[정보] 입력 소스: 파일: sample/sample_email.txt (1,234 bytes)
[정보] 텍스트 길이: 1,234자
[정보] 요약 설정: 길이=short, 언어=ko, 강조=False
[정보] 텍스트 미리보기: 제목: [회의 안내] 2024년 1분기 프로젝트 진행 상황 점검 회의...
──────────────────────────────────────────────────

📝 요약 결과:

2024년 1분기 프로젝트 진행 상황을 점검하고 2분기 계획을 수립하기 위한 회의를 개최하고자 합니다. 회의 일정: - 일시: 2024년 4월 15일 (월) 오후 2시 ~ 4시 - 장소: 3층 대회의실 - 참석자: 개발팀 전체, 기획팀 대표, 디자인팀 대표. 회의 안건: 1. 1분기 프로젝트 진행 상황 리뷰 2. 2분기 프로젝트 계획 수립 3. 팀 운영 개선사항 논의.

🔑 주요 키워드:
  • 회의 (5회)
  • 프로젝트 (4회)
  • 진행 (3회)
  • 계획 (2회)
  • 팀 (2회)

📊 요약 통계:
  • 원본 길이: 1,234자
  • 요약 길이: 456자
  • 압축률: 63.0%
  • 문장 수: 15개 → 3개
```

## 🎯 다음 단계

현재 **3단계까지 완료**되었으며, 다음은 **4단계: 키워드 추출 및 강조 기능 추가**입니다.

### 3단계 구현 완료 내용
- ✅ 문장 추출 기반 요약 알고리즘
- ✅ 키워드 추출 및 빈도수 계산
- ✅ 문장 중요도 점수 계산
- ✅ 요약 길이 조절 (short/long)
- ✅ 키워드 강조 출력
- ✅ 상세한 통계 정보 제공

### 4단계 구현 계획
1. 키워드 추출 알고리즘 개선 (TF-IDF, Word2Vec 등)
2. 키워드 강조 출력 개선 (색상, 굵기 등)
3. 중요도 기반 정렬 및 필터링
4. 다국어 키워드 추출 지원

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