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

### ✅ 4단계: TF-IDF 기반 키워드 추출 및 강조 기능 추가
- [x] TF-IDF 알고리즘 구현 (단어 빈도 × 역문서빈도)
- [x] 향상된 키워드 강조 (중요도별 색상 구분)
- [x] 중요도 기반 정렬 및 점수 표시
- [x] 개선된 문장 중요도 분석 (위치, 길이, 패턴 매칭)
- [x] CLI 구조 개선 (직관적인 명령어)

### ⏳ 5단계: 다국어 지원 및 고급 기능
- [ ] 영어 텍스트 처리 개선
- [ ] 더 정교한 불용어 처리
- [ ] 문장 유사도 분석
- [ ] 요약 품질 평가 기능

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

# 파일에서 요약
python -m email_summarizer sample/sample.txt
```

## 📖 현재 사용법

### 기본 사용법
```bash
# 파일에서 텍스트 요약
python -m email_summarizer sample/sample.txt

# 상세 정보와 함께 요약
python -m email_summarizer sample/sample.txt --verbose

# 긴 요약
python -m email_summarizer sample/sample.txt --length long

# 키워드 강조 (색상 및 굵기)
python -m email_summarizer sample/sample.txt --highlight

# 모든 옵션 조합
python -m email_summarizer sample/sample.txt --length long --highlight --verbose
```

### 현재 지원하는 옵션
| 옵션 | 축약 | 설명 | 기본값 |
|------|------|------|--------|
| `FILE` | - | 요약할 텍스트 파일 경로 | None |
| `--length` | `-l` | 요약 길이: `short` 또는 `long` | `short` |
| `--language` | `--lang` | 요약 언어: `ko` 또는 `en` | `ko` |
| `--highlight` | `-h` | 키워드 강조 출력 (색상 및 굵기) | `False` |
| `--verbose` | `-v` | 상세 정보 출력 | `False` |

## 🏗️ 프로젝트 구조
```
email-summarizer-cli/
├── email_summarizer/
│   ├── __init__.py          # 패키지 초기화
│   ├── __main__.py          # 모듈 실행 엔트리포인트
│   ├── cli.py              # Typer CLI 구현 ✅
│   ├── utils.py            # 입력 처리 및 유틸리티 함수 ✅
│   └── summarizer.py       # 요약 로직 (TF-IDF 포함) ✅
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
- **TF-IDF** - 키워드 추출 알고리즘
- **정규표현식** - 텍스트 처리 및 문장 분리

## 🧪 현재 테스트 가능한 기능

### 다양한 텍스트 요약 테스트
```bash
# 기본 샘플 텍스트 (TF-IDF 키워드 추출)
python -m email_summarizer sample/sample.txt --highlight --verbose

# 이메일 형태 텍스트
python -m email_summarizer sample/sample_email.txt --verbose

# 기술 문서 형태 텍스트
python -m email_summarizer sample/sample_article.txt --highlight

# 오류 처리 테스트
python -m email_summarizer nonexistent.txt

# 빈 파일 테스트
echo "" > empty.txt
python -m email_summarizer empty.txt
```

### 현재 출력 예시 (4단계 완료 후)
```
📁 파일 읽는 중: sample\sample.txt
✅ 파일 읽기 완료 (517자)
🔍 텍스트 검증 완료
📊 요약 설정: 길이=short, 언어=ko, 강조=True
🤖 AI 요약 생성 중...
✅ 요약 생성 완료

📝 요약 결과:

이 **시스템은** 자연어 처리 기술을 활용하여 긴 텍스트를 간결하게 요약하는 **기능을** 제공합니다. 주요 특징으로는 키워드 추출, 문장 중요도 분석, 그리고 다양한 길이의 요약 생성이 있습니다. 개발 과정에서 가장 **중요한** 것은 사용자 경험을 고려한 직관적인 인터페이스 설계입니다.

🔑 주요 키워드 (중요도 순):
  1. **시스템은** (점수: 0.52)
  2. **기능을** (점수: 0.52)
  3. **시스템의** (점수: 0.52)
  4. **중요한** (점수: 0.52)
  5. **시스템에** (점수: 0.52)

📊 요약 통계:
  • 원본 길이: 517자
  • 요약 길이: 151자
  • 압축률: 70.8%
  • 문장 수: 12개 → 3개
```

## 🎯 다음 단계

현재 **4단계까지 완료**되었으며, 다음은 **5단계: 다국어 지원 및 고급 기능**입니다.

### 4단계 구현 완료 내용
- ✅ TF-IDF 기반 키워드 추출 알고리즘
- ✅ 향상된 키워드 강조 (중요도별 색상 구분)
- ✅ 중요도 기반 정렬 및 점수 표시
- ✅ 개선된 문장 중요도 분석 (위치, 길이, 패턴 매칭)
- ✅ CLI 구조 개선 (직관적인 명령어)
- ✅ 상세한 통계 정보 제공

### 5단계 구현 계획
1. 영어 텍스트 처리 개선 및 다국어 지원 확대
2. 더 정교한 불용어 처리 및 문장 유사도 분석
3. 요약 품질 평가 기능 추가
4. 웹 API 인터페이스 개발

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