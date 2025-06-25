# 요약 및 키워드 추출 로직 

import re
from typing import List, Tuple, Dict
from collections import Counter
import math


def split_sentences(text: str) -> List[str]:
    """
    텍스트를 문장 단위로 분리합니다.
    
    Args:
        text: 분리할 텍스트
        
    Returns:
        List[str]: 문장 리스트
    """
    # 문장 끝 패턴 (마침표, 느낌표, 물음표)
    sentence_pattern = r'[.!?]+'
    
    # 문장 분리
    sentences = re.split(sentence_pattern, text)
    
    # 빈 문장 제거 및 공백 정리
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences


def extract_words(text: str) -> List[str]:
    """
    텍스트에서 단어를 추출합니다.
    
    Args:
        text: 단어를 추출할 텍스트
        
    Returns:
        List[str]: 단어 리스트
    """
    # 한글, 영문, 숫자만 추출
    words = re.findall(r'[가-힣a-zA-Z0-9]+', text.lower())
    
    # 불용어 제거
    stopwords = {
        '이', '그', '저', '것', '수', '등', '때', '곳', '말', '일', '년', '월', '일',
        '시', '분', '초', '개', '명', '번', '회', '차', '대', '마리', '권', '채',
        '그것', '이것', '저것', '무엇', '어떤', '어떻게', '왜', '언제', '어디서',
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
        'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        '그리고', '또는', '하지만', '그런데', '그러나', '따라서', '그래서', '그러면',
        '이제', '지금', '오늘', '내일', '어제', '여기', '저기', '거기', '어디'
    }
    
    # 불용어 제거 및 길이 필터링
    words = [word for word in words if word not in stopwords and len(word) > 1]
    
    return words


def calculate_tf_idf_keywords(text: str, top_n: int = 10) -> List[Tuple[str, float]]:
    """
    TF-IDF 기반으로 키워드를 추출합니다.
    
    Args:
        text: 키워드를 추출할 텍스트
        top_n: 추출할 키워드 개수
        
    Returns:
        List[Tuple[str, float]]: (키워드, TF-IDF 점수) 리스트
    """
    # 문장 분리
    sentences = split_sentences(text)
    if not sentences:
        return []
    
    # 각 문장에서 단어 추출
    sentence_words = [extract_words(sentence) for sentence in sentences]
    
    # 전체 단어 리스트
    all_words = extract_words(text)
    total_words = len(all_words)
    
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
        
        # 추가 가중치 (특별한 패턴)
        bonus = 0.0
        if re.search(r'주요|핵심|중요|특징|기능|목적|의미|개발|시스템|프로젝트', word):
            bonus += 0.5
        if re.search(r'api|web|app|database|server|client|framework', word.lower()):
            bonus += 0.3
        
        word_scores[word] = tf_idf + bonus
    
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
    words = extract_words(text)
    word_counts = Counter(words)
    return word_counts.most_common(top_n)


def calculate_sentence_score(sentence: str, keywords: List[Tuple[str, float]]) -> float:
    """
    문장의 중요도를 계산합니다. (개선된 버전)
    
    Args:
        sentence: 점수를 계산할 문장
        keywords: 키워드 리스트 (TF-IDF 점수 포함)
        
    Returns:
        float: 문장 점수
    """
    sentence_lower = sentence.lower()
    score = 0.0
    
    # 키워드 포함 점수 (TF-IDF 점수 반영)
    for keyword, tf_idf_score in keywords:
        if keyword in sentence_lower:
            score += tf_idf_score * 2  # TF-IDF 점수에 가중치
    
    # 문장 길이 점수 (최적 길이 범위)
    length = len(sentence)
    if 15 <= length <= 120:
        score += 1.5
    elif 10 <= length < 15 or 120 < length <= 200:
        score += 1.0
    elif length < 10:
        score += 0.3
    
    # 특별한 패턴 점수
    important_patterns = [
        (r'주요|핵심|중요|특징|기능|목적|의미', 3.0),
        (r'예시|예를|예시로|구체적으로', 2.0),
        (r'개발|구현|설계|아키텍처', 2.5),
        (r'최적화|성능|보안|테스트', 2.0),
        (r'결론|요약|정리', 1.5)
    ]
    
    for pattern, pattern_score in important_patterns:
        if re.search(pattern, sentence):
            score += pattern_score
    
    # 위치 점수 (문장의 위치에 따른 가중치)
    sentences = split_sentences(sentence)
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


def summarize_text(text: str, length: str = "short", language: str = "ko") -> Dict:
    """
    텍스트를 요약합니다.
    
    Args:
        text: 요약할 텍스트
        length: 요약 길이 ("short" 또는 "long")
        language: 언어 ("ko" 또는 "en")
        
    Returns:
        Dict: 요약 결과
    """
    # 문장 분리
    sentences = split_sentences(text)
    
    if not sentences:
        return {
            "summary": "요약할 내용이 없습니다.",
            "keywords": [],
            "original_length": len(text),
            "summary_length": 0
        }
    
    # TF-IDF 기반 키워드 추출
    keywords_tfidf = calculate_tf_idf_keywords(text)
    
    # 문장 점수 계산
    sentence_scores = []
    for sentence in sentences:
        score = calculate_sentence_score(sentence, keywords_tfidf)
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
        "selected_sentences": len(selected_sentences)
    }


def format_summary_output(summary_result: Dict, highlight: bool = False) -> str:
    """
    요약 결과를 포맷팅합니다. (개선된 버전)
    
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
        # 키워드 강조된 요약 (색상 및 굵기)
        summary_text = summary_result["summary"]
        for keyword, score in summary_result["keywords"]:
            # 중요도에 따른 강조 스타일
            if score > 1.0:
                summary_text = summary_text.replace(
                    keyword, f"\033[1;33m**{keyword}**\033[0m"  # 노란색 굵게
                )
            else:
                summary_text = summary_text.replace(
                    keyword, f"\033[1;36m**{keyword}**\033[0m"  # 청록색 굵게
                )
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
    
    # 통계 정보
    output.append("📊 요약 통계:")
    output.append(f"  • 원본 길이: {summary_result['original_length']:,}자")
    output.append(f"  • 요약 길이: {summary_result['summary_length']:,}자")
    output.append(f"  • 압축률: {((1 - summary_result['summary_length'] / summary_result['original_length']) * 100):.1f}%")
    output.append(f"  • 문장 수: {summary_result['sentence_count']}개 → {summary_result['selected_sentences']}개")
    
    return "\n".join(output) 