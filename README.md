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

### 🔄 3단계: 간단한 요약 알고리즘으로 MVP 동작 확인 (진행 예정)
- [ ] 문장 추출 기반 요약 로직
- [ ] 기본 출력 포맷 구현
- [ ] MVP 동작 테스트

### ⏳ 4단계: 키워드 추출 및 강조 기능 추가
- [ ] 키워드 추출 알고리즘
- [ ] 키워드 강조 출력
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

## �� 현재 사용법

### 기본 사용법
```bash
# 파일에서 텍스트 요약 (현재는 미리보기만)
python -m email_summarizer summarize --input sample.txt

# 상세 정보와 함께 요약
python -m email_summarizer summarize --input sample.txt --verbose

# 다른 옵션들 (아직 요약 로직 미구현)
python -m email_summarizer summarize --input sample.txt --length long --language en
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
│   └── summarizer.py       # 요약 로직 (구현 예정) 🔄
├── tests/
│   └── test_summarizer.py  # 테스트 코드 (작성 예정) ⏳
├── sample.txt              # 테스트용 샘플 파일
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

### 입력 처리 테스트
```bash
# 정상 파일 입력 (권장)
python -m email_summarizer summarize --input sample.txt --verbose

# 오류 처리 테스트
python -m email_summarizer summarize --input nonexistent.txt

# 빈 파일 테스트
echo "" > empty.txt
python -m email_summarizer summarize --input empty.txt

# 인코딩 테스트 (다양한 인코딩 지원)
python -m email_summarizer summarize --input sample.txt --verbose
```

### 현재 출력 예시
```
[정보] 입력 소스: 파일: sample.txt (393 bytes)
[정보] 텍스트 길이: 393자
[정보] 요약 설정: 길이=short, 언어=ko, 강조=False
[정보] 텍스트 미리보기: 안녕하세요! 이것은 AI 기반 이메일/메시지 요약 CLI 도구의 테스트를 위한 샘플 텍스트입니다...
──────────────────────────────────────────────────
[DEBUG] 요약 시작 - 텍스트 길이: 393자
[DEBUG] 설정: length=short, language=ko, highlight=False

📝 요약 결과:
(요약 로직이 아직 구현되지 않았습니다)
입력 텍스트: 안녕하세요! 이것은 AI 기반 이메일/메시지 요약 CLI 도구의 테스트를 위한 샘플 텍스트입니다...
```

## 🎯 다음 단계

현재 **2단계까지 완료**되었으며, 다음은 **3단계: 간단한 요약 알고리즘 구현**입니다.

### 3단계 구현 계획
1. `summarizer.py` 파일 생성
2. 문장 추출 기반 요약 로직 구현
3. CLI와 요약 로직 연동
4. 기본 출력 포맷 구현

### 예상 결과
```bash
python -m email_summarizer summarize --input sample.txt --verbose
```
실행 시 실제 요약 결과가 출력될 예정입니다.

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