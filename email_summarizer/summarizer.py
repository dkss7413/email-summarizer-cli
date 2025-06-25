# 요약 및 키워드 추출 로직 

import re
from typing import List, Tuple, Dict
from collections import Counter
import math


def detect_language(text: str) -> str:
    """
    텍스트의 언어를 감지합니다.
    
    Args:
        text: 언어를 감지할 텍스트
        
    Returns:
        str: 감지된 언어 ('ko', 'en', 'mixed')
    """
    # 한글 문자 패턴
    korean_pattern = r'[가-힣]'
    # 영문 문자 패턴
    english_pattern = r'[a-zA-Z]'
    
    korean_count = len(re.findall(korean_pattern, text))
    english_count = len(re.findall(english_pattern, text))
    
    total_chars = len(re.findall(r'[가-힣a-zA-Z]', text))
    
    if total_chars == 0:
        return 'ko'  # 기본값
    
    korean_ratio = korean_count / total_chars
    english_ratio = english_count / total_chars
    
    if korean_ratio > 0.7:
        return 'ko'
    elif english_ratio > 0.7:
        return 'en'
    else:
        return 'mixed'


def get_stopwords(language: str) -> set:
    """
    언어별 불용어 목록을 반환합니다.
    
    Args:
        language: 언어 ('ko', 'en', 'mixed')
        
    Returns:
        set: 불용어 집합
    """
    korean_stopwords = {
        # 기본 불용어
        '이', '그', '저', '것', '수', '등', '때', '곳', '말', '일', '년', '월', '일',
        '시', '분', '초', '개', '명', '번', '회', '차', '대', '마리', '권', '채',
        '그것', '이것', '저것', '무엇', '어떤', '어떻게', '왜', '언제', '어디서',
        '그리고', '또는', '하지만', '그런데', '그러나', '따라서', '그래서', '그러면',
        '이제', '지금', '오늘', '내일', '어제', '여기', '저기', '거기', '어디',
        
        # 조사
        '은', '는', '이', '가', '을', '를', '의', '에', '에서', '로', '으로', '와', '과',
        '도', '만', '부터', '까지', '보다', '처럼', '같이', '마다', '마다', '마다',
        
        # 접속사
        '그리고', '또는', '하지만', '그런데', '그러나', '따라서', '그래서', '그러면',
        '만약', '만일', '만약에', '만일', '만약에', '만일', '만약에', '만일',
        
        # 부사
        '매우', '너무', '아주', '정말', '진짜', '완전', '전혀', '절대', '아직', '벌써',
        '곧', '바로', '즉시', '당장', '지금', '이제', '오늘', '내일', '어제',
        
        # 대명사
        '나', '너', '우리', '저희', '그들', '그녀', '그', '이', '저', '누구', '무엇',
        '어떤', '어떻게', '왜', '언제', '어디서', '어디', '어떤', '어떻게',
        
        # 수사
        '하나', '둘', '셋', '넷', '다섯', '여섯', '일곱', '여덟', '아홉', '열',
        '첫째', '둘째', '셋째', '넷째', '다섯째', '여섯째', '일곱째', '여덟째', '아홉째', '열째',
        
        # 기타
        '있다', '없다', '하다', '되다', '있다', '없다', '하다', '되다',
        '있다', '없다', '하다', '되다', '있다', '없다', '하다', '되다'
    }
    
    english_stopwords = {
        # 기본 불용어
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
        'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'must', 'can', 'shall', 'ought', 'need', 'dare',
        
        # 접속사
        'and', 'or', 'but', 'nor', 'yet', 'so', 'although', 'because', 'since',
        'unless', 'while', 'where', 'when', 'if', 'then', 'else', 'though',
        
        # 전치사
        'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about',
        'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between',
        'among', 'within', 'without', 'against', 'toward', 'towards', 'upon',
        
        # 대명사
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his',
        'hers', 'ours', 'theirs', 'this', 'that', 'these', 'those', 'who', 'whom',
        'whose', 'which', 'what', 'where', 'when', 'why', 'how',
        
        # 부사
        'very', 'too', 'so', 'quite', 'rather', 'really', 'just', 'only', 'even',
        'still', 'already', 'yet', 'now', 'then', 'here', 'there', 'where',
        'when', 'why', 'how', 'well', 'badly', 'quickly', 'slowly', 'easily',
        
        # 조동사
        'can', 'could', 'may', 'might', 'will', 'would', 'shall', 'should',
        'must', 'ought', 'need', 'dare', 'used',
        
        # 기타
        'yes', 'no', 'not', 'n\'t', 'all', 'any', 'both', 'each', 'few', 'more',
        'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
        'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
        'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain',
        'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn',
        'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren',
        'won', 'wouldn'
    }
    
    if language == 'ko':
        return korean_stopwords
    elif language == 'en':
        return english_stopwords
    else:  # mixed
        return korean_stopwords.union(english_stopwords)


def extract_words(text: str, language: str = 'ko') -> List[str]:
    """
    텍스트에서 단어를 추출합니다. (언어별 최적화)
    
    Args:
        text: 단어를 추출할 텍스트
        language: 언어 ('ko', 'en', 'mixed')
        
    Returns:
        List[str]: 단어 리스트
    """
    # 언어별 단어 추출 패턴
    if language == 'ko':
        # 한글, 영문, 숫자 추출
        words = re.findall(r'[가-힣a-zA-Z0-9]+', text.lower())
    elif language == 'en':
        # 영문, 숫자만 추출 (더 엄격한 영문 처리)
        words = re.findall(r'[a-zA-Z]+', text.lower())
    else:  # mixed
        # 한글, 영문, 숫자 추출
        words = re.findall(r'[가-힣a-zA-Z0-9]+', text.lower())
    
    # 불용어 제거
    stopwords = get_stopwords(language)
    
    # 불용어 제거 및 길이 필터링
    filtered_words = []
    for word in words:
        # 길이 필터링 (한글: 2자 이상, 영문: 3자 이상)
        min_length = 2 if language == 'ko' else 3
        if len(word) >= min_length and word not in stopwords:
            filtered_words.append(word)
    
    return filtered_words


def split_sentences(text: str, language: str = 'ko') -> List[str]:
    """
    텍스트를 문장 단위로 분리합니다. (언어별 최적화)
    
    Args:
        text: 분리할 텍스트
        language: 언어 ('ko', 'en', 'mixed')
        
    Returns:
        List[str]: 문장 리스트
    """
    if language == 'ko':
        # 한글 문장 끝 패턴
        sentence_pattern = r'[.!?]+'
    elif language == 'en':
        # 영문 문장 끝 패턴 (더 정교한 처리)
        sentence_pattern = r'[.!?]+(?=\s|$)'
    else:  # mixed
        # 혼합 언어 문장 끝 패턴
        sentence_pattern = r'[.!?]+'
    
    # 문장 분리
    sentences = re.split(sentence_pattern, text)
    
    # 빈 문장 제거 및 공백 정리
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences


def calculate_tf_idf_keywords(text: str, top_n: int = 10, language: str = 'ko') -> List[Tuple[str, float]]:
    """
    TF-IDF 기반으로 키워드를 추출합니다. (언어별 최적화)
    
    Args:
        text: 키워드를 추출할 텍스트
        top_n: 추출할 키워드 개수
        language: 언어 ('ko', 'en', 'mixed')
        
    Returns:
        List[Tuple[str, float]]: (키워드, TF-IDF 점수) 리스트
    """
    # 언어 감지 (자동 감지가 우선)
    detected_lang = detect_language(text)
    if language == 'auto':
        language = detected_lang
    
    # 문장 분리
    sentences = split_sentences(text, language)
    if not sentences:
        return []
    
    # 각 문장에서 단어 추출
    sentence_words = [extract_words(sentence, language) for sentence in sentences]
    
    # 전체 단어 리스트
    all_words = extract_words(text, language)
    total_words = len(all_words)
    
    if total_words == 0:
        return []
    
    # 단어별 TF-IDF 점수 계산
    word_scores = {}
    
    for word in set(all_words):
        # TF (Term Frequency) 계산
        tf = all_words.count(word) / total_words
        
        # IDF (Inverse Document Frequency) 계산
        sentences_with_word = sum(1 for words in sentence_words if word in words)
        idf = math.log(len(sentences) / (sentences_with_word + 1))
        
        # TF-IDF 점수
        tf_idf = tf * idf
        
        # 언어별 추가 가중치
        bonus = 0.0
        
        if language == 'ko':
            # 한글 특별 패턴
            if re.search(r'주요|핵심|중요|특징|기능|목적|의미|개발|시스템|프로젝트', word):
                bonus += 0.5
            if re.search(r'개선|최적화|성능|보안|테스트|분석', word):
                bonus += 0.3
        elif language == 'en':
            # 영문 특별 패턴
            if re.search(r'important|key|main|primary|essential|critical|major', word.lower()):
                bonus += 0.5
            if re.search(r'feature|function|system|project|development|analysis', word.lower()):
                bonus += 0.3
            if re.search(r'api|web|app|database|server|client|framework', word.lower()):
                bonus += 0.2
        else:  # mixed
            # 혼합 언어 패턴
            if re.search(r'주요|핵심|중요|특징|기능|목적|의미|개발|시스템|프로젝트|important|key|main|primary|essential', word.lower()):
                bonus += 0.5
            if re.search(r'api|web|app|database|server|client|framework', word.lower()):
                bonus += 0.3
        
        word_scores[word] = tf_idf + bonus
    
    # 영어의 경우 단수형과 복수형 통합
    if language == 'en':
        # 단수형과 복수형 매핑
        singular_forms = {}
        for word in list(word_scores.keys()):  # keys()를 list로 복사
            if word.endswith('s') and len(word) > 3:
                # 복수형인 경우 단수형 찾기
                singular = word[:-1]  # s 제거
                if singular in word_scores:
                    # 단수형과 복수형 점수 합산
                    combined_score = word_scores[word] + word_scores[singular]
                    singular_forms[singular] = combined_score
                    # 복수형 제거
                    del word_scores[word]
                else:
                    # 단수형이 없는 경우 그대로 유지
                    pass
            elif not word.endswith('s') and len(word) > 2:
                # 단수형인 경우 복수형 확인
                plural = word + 's'
                if plural in word_scores:
                    # 이미 복수형에서 처리됨
                    pass
                else:
                    # 단수형만 있는 경우
                    singular_forms[word] = word_scores[word]
        # 통합된 점수로 업데이트
        for word, score in singular_forms.items():
            word_scores[word] = score
    
    # 점수 순으로 정렬하여 상위 N개 반환
    sorted_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_words[:top_n]


def extract_keywords(text: str, top_n: int = 10) -> List[Tuple[str, int]]:
    """
    텍스트에서 키워드를 추출합니다. (기존 방식 - 호환성 유지)
    
    Args:
        text: 키워드를 추출할 텍스트
        top_n: 추출할 키워드 개수
        
    Returns:
        List[Tuple[str, int]]: (키워드, 빈도수) 리스트
    """
    language = detect_language(text)
    words = extract_words(text, language)
    word_counts = Counter(words)
    return word_counts.most_common(top_n)


def calculate_sentence_score(sentence: str, keywords: List[Tuple[str, float]], language: str = 'ko') -> float:
    """
    문장의 중요도를 계산합니다. (언어별 최적화)
    
    Args:
        sentence: 점수를 계산할 문장
        keywords: 키워드 리스트 (TF-IDF 점수 포함)
        language: 언어 ('ko', 'en', 'mixed')
        
    Returns:
        float: 문장 점수
    """
    sentence_lower = sentence.lower()
    score = 0.0
    
    # 키워드 포함 점수 (TF-IDF 점수 반영)
    for keyword, tf_idf_score in keywords:
        if keyword in sentence_lower:
            score += tf_idf_score * 2  # TF-IDF 점수에 가중치
    
    # 문장 길이 점수 (언어별 최적 길이)
    length = len(sentence)
    if language == 'ko':
        if 15 <= length <= 120:
            score += 1.5
        elif 10 <= length < 15 or 120 < length <= 200:
            score += 1.0
        elif length < 10:
            score += 0.3
    elif language == 'en':
        if 20 <= length <= 150:
            score += 1.5
        elif 15 <= length < 20 or 150 < length <= 250:
            score += 1.0
        elif length < 15:
            score += 0.3
    else:  # mixed
        if 15 <= length <= 120:
            score += 1.5
        elif 10 <= length < 15 or 120 < length <= 200:
            score += 1.0
        elif length < 10:
            score += 0.3
    
    # 언어별 특별한 패턴 점수
    if language == 'ko':
        important_patterns = [
            (r'주요|핵심|중요|특징|기능|목적|의미', 3.0),
            (r'예시|예를|예시로|구체적으로', 2.0),
            (r'개발|구현|설계|아키텍처', 2.5),
            (r'최적화|성능|보안|테스트', 2.0),
            (r'결론|요약|정리', 1.5)
        ]
    elif language == 'en':
        important_patterns = [
            (r'important|key|main|primary|essential|critical', 3.0),
            (r'example|instance|specifically|concretely', 2.0),
            (r'develop|implement|design|architecture', 2.5),
            (r'optimize|performance|security|test', 2.0),
            (r'conclusion|summary|conclude', 1.5)
        ]
    else:  # mixed
        important_patterns = [
            (r'주요|핵심|중요|특징|기능|목적|의미|important|key|main|primary|essential', 3.0),
            (r'예시|예를|예시로|구체적으로|example|instance|specifically', 2.0),
            (r'개발|구현|설계|아키텍처|develop|implement|design|architecture', 2.5),
            (r'최적화|성능|보안|테스트|optimize|performance|security|test', 2.0),
            (r'결론|요약|정리|conclusion|summary|conclude', 1.5)
        ]
    
    for pattern, pattern_score in important_patterns:
        if re.search(pattern, sentence, re.IGNORECASE):
            score += pattern_score
    
    # 위치 점수 (문장의 위치에 따른 가중치)
    sentences = split_sentences(sentence, language)
    if sentences:
        sentence_index = sentences.index(sentence) if sentence in sentences else 0
        total_sentences = len(sentences)
        
        # 첫 번째 문장과 마지막 문장에 가중치
        if sentence_index == 0:
            score += 1.0
        elif sentence_index == total_sentences - 1:
            score += 0.8
        elif sentence_index < total_sentences * 0.3:  # 앞부분
            score += 0.5
    
    return score


def summarize_text(text: str, length: str = "short", language: str = "auto") -> Dict:
    """
    텍스트를 요약합니다. (언어별 최적화)
    
    Args:
        text: 요약할 텍스트
        length: 요약 길이 ("short" 또는 "long")
        language: 언어 ("ko", "en", "mixed", "auto")
        
    Returns:
        Dict: 요약 결과
    """
    # 언어 감지
    detected_language = detect_language(text)
    if language == "auto":
        language = detected_language
    
    # 문장 분리
    sentences = split_sentences(text, language)
    
    if not sentences:
        return {
            "summary": "요약할 내용이 없습니다.",
            "keywords": [],
            "original_length": len(text),
            "summary_length": 0,
            "detected_language": language
        }
    
    # TF-IDF 기반 키워드 추출
    keywords_tfidf = calculate_tf_idf_keywords(text, language=language)
    
    # 문장 점수 계산
    sentence_scores = []
    for sentence in sentences:
        score = calculate_sentence_score(sentence, keywords_tfidf, language)
        sentence_scores.append((sentence, score))
    
    # 점수 순으로 정렬
    sentence_scores.sort(key=lambda x: x[1], reverse=True)
    
    # 요약 길이 결정
    if length == "short":
        summary_count = min(3, len(sentences))
    else:  # long
        summary_count = min(5, len(sentences))
    
    # 상위 문장들 선택
    selected_sentences = sentence_scores[:summary_count]
    
    # 원래 순서대로 정렬
    selected_sentences.sort(key=lambda x: sentences.index(x[0]))
    
    # 요약 텍스트 생성
    summary_text = ". ".join([s[0] for s in selected_sentences]) + "."
    
    return {
        "summary": summary_text,
        "keywords": keywords_tfidf[:5],  # 상위 5개 키워드
        "original_length": len(text),
        "summary_length": len(summary_text),
        "sentence_count": len(sentences),
        "selected_sentences": len(selected_sentences),
        "detected_language": detected_language,
        "processing_language": language
    }


def format_summary_output(summary_result: Dict, highlight: bool = False) -> str:
    """
    요약 결과를 포맷팅합니다. (언어 정보 포함)
    
    Args:
        summary_result: 요약 결과 딕셔너리
        highlight: 키워드 강조 여부
        
    Returns:
        str: 포맷팅된 요약 결과
    """
    output = []
    
    # 요약 텍스트
    output.append("📝 요약 결과:")
    output.append("")
    
    if highlight and summary_result["keywords"]:
        summary_text = summary_result["summary"]
        detected_lang = summary_result.get("detected_language", "ko")
        
        # 긴 키워드부터 정렬 (중첩 방지)
        sorted_keywords = sorted(summary_result["keywords"], key=lambda x: -len(x[0]))
        import re
        for keyword, score in sorted_keywords:
            if score > 1.0:
                highlight_style = f"\033[1;33m**{keyword}**\033[0m"
            else:
                highlight_style = f"\033[1;36m**{keyword}**\033[0m"
            if detected_lang == "en":
                # negative lookbehind: 강조된 부분(이스케이프 시퀀스) 뒤가 아닌 곳만 매칭
                # (?<!\033\[1;33m\*\*) 등으로 이미 강조된 부분 제외
                # 단, lookbehind는 고정 길이만 지원하므로, 강조 패턴을 단순화
                pattern = re.compile(r'(?<!\*\*)(?<!\033\[1;33m\*\*)(?<!\033\[1;36m\*\*)' + re.escape(keyword) + r'(?!\*\*)(?!\033\[0m)', re.IGNORECASE)
                summary_text = pattern.sub(highlight_style, summary_text)
                if not keyword.endswith('s'):
                    plural_keyword = keyword + 's'
                    plural_style = f"\033[1;33m**{plural_keyword}**\033[0m" if score > 1.0 else f"\033[1;36m**{plural_keyword}**\033[0m"
                    pattern_plural = re.compile(r'(?<!\*\*)(?<!\033\[1;33m\*\*)(?<!\033\[1;36m\*\*)' + re.escape(plural_keyword) + r'(?!\*\*)(?!\033\[0m)', re.IGNORECASE)
                    summary_text = pattern_plural.sub(plural_style, summary_text)
            else:
                # 한글/혼합: 기존 방식, 단 이미 강조된 부분은 건너뜀
                def replacer_ko(m):
                    if '\033[' in m.group(0):
                        return m.group(0)
                    return highlight_style
                pattern_ko = re.compile(re.escape(keyword))
                summary_text = pattern_ko.sub(replacer_ko, summary_text)
        output.append(summary_text)
    else:
        output.append(summary_result["summary"])
    
    output.append("")
    
    # 키워드 (중요도 순)
    if summary_result["keywords"]:
        output.append("🔑 주요 키워드 (중요도 순):")
        for i, (keyword, score) in enumerate(summary_result["keywords"], 1):
            if highlight:
                if score > 1.0:
                    output.append(f"  {i}. \033[1;33m**{keyword}**\033[0m (점수: {score:.2f})")
                else:
                    output.append(f"  {i}. \033[1;36m**{keyword}**\033[0m (점수: {score:.2f})")
            else:
                output.append(f"  {i}. {keyword} (점수: {score:.2f})")
        output.append("")
    
    # 언어 정보
    if "detected_language" in summary_result:
        lang_names = {"ko": "한국어", "en": "영어", "mixed": "혼합 언어"}
        detected = lang_names.get(summary_result["detected_language"], summary_result["detected_language"])
        processing = lang_names.get(summary_result["processing_language"], summary_result["processing_language"])
        output.append(f"🌐 언어 정보: 감지됨={detected}, 처리됨={processing}")
        output.append("")
    
    # 통계 정보
    output.append("📊 요약 통계:")
    output.append(f"  • 원본 길이: {summary_result['original_length']:,}자")
    output.append(f"  • 요약 길이: {summary_result['summary_length']:,}자")
    output.append(f"  • 압축률: {((1 - summary_result['summary_length'] / summary_result['original_length']) * 100):.1f}%")
    output.append(f"  • 문장 수: {summary_result['sentence_count']}개 → {summary_result['selected_sentences']}개")
    
    return "\n".join(output) 