# 요약 및 키워드 추출 로직 

import re
from typing import List, Tuple, Dict
from collections import Counter


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


def extract_keywords(text: str, top_n: int = 10) -> List[Tuple[str, int]]:
    """
    텍스트에서 키워드를 추출합니다.
    
    Args:
        text: 키워드를 추출할 텍스트
        top_n: 추출할 키워드 개수
        
    Returns:
        List[Tuple[str, int]]: (키워드, 빈도수) 리스트
    """
    # 한글, 영문, 숫자만 추출
    words = re.findall(r'[가-힣a-zA-Z0-9]+', text.lower())
    
    # 불용어 제거 (한글)
    stopwords = {
        '이', '그', '저', '것', '수', '등', '때', '곳', '말', '일', '년', '월', '일',
        '시', '분', '초', '개', '명', '번', '회', '차', '대', '마리', '권', '채',
        '그것', '이것', '저것', '무엇', '어떤', '어떻게', '왜', '언제', '어디서',
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
        'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
    }
    
    # 불용어 제거
    words = [word for word in words if word not in stopwords and len(word) > 1]
    
    # 빈도수 계산
    word_counts = Counter(words)
    
    # 상위 N개 반환
    return word_counts.most_common(top_n)


def calculate_sentence_score(sentence: str, keywords: List[Tuple[str, int]]) -> float:
    """
    문장의 중요도를 계산합니다.
    
    Args:
        sentence: 점수를 계산할 문장
        keywords: 키워드 리스트
        
    Returns:
        float: 문장 점수
    """
    sentence_lower = sentence.lower()
    score = 0.0
    
    # 키워드 포함 점수
    for keyword, frequency in keywords:
        if keyword in sentence_lower:
            score += frequency
    
    # 문장 길이 점수 (너무 짧거나 긴 문장은 낮은 점수)
    length = len(sentence)
    if 10 <= length <= 100:
        score += 1.0
    elif 5 <= length < 10 or 100 < length <= 200:
        score += 0.5
    
    # 특별한 패턴 점수
    if re.search(r'주요|핵심|중요|특징|기능|목적|의미', sentence):
        score += 2.0
    
    if re.search(r'예시|예를|예시로|구체적으로', sentence):
        score += 1.5
    
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
    
    # 키워드 추출
    keywords = extract_keywords(text)
    
    # 문장 점수 계산
    sentence_scores = []
    for sentence in sentences:
        score = calculate_sentence_score(sentence, keywords)
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
        "keywords": keywords[:5],  # 상위 5개 키워드
        "original_length": len(text),
        "summary_length": len(summary_text),
        "sentence_count": len(sentences),
        "selected_sentences": len(selected_sentences)
    }


def format_summary_output(summary_result: Dict, highlight: bool = False) -> str:
    """
    요약 결과를 포맷팅합니다.
    
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
        # 키워드 강조된 요약
        summary_text = summary_result["summary"]
        for keyword, _ in summary_result["keywords"]:
            summary_text = summary_text.replace(
                keyword, f"**{keyword}**"
            )
        output.append(summary_text)
    else:
        output.append(summary_result["summary"])
    
    output.append("")
    
    # 키워드
    if summary_result["keywords"]:
        output.append("🔑 주요 키워드:")
        for keyword, frequency in summary_result["keywords"]:
            if highlight:
                output.append(f"  • **{keyword}** ({frequency}회)")
            else:
                output.append(f"  • {keyword} ({frequency}회)")
        output.append("")
    
    # 통계 정보
    output.append("📊 요약 통계:")
    output.append(f"  • 원본 길이: {summary_result['original_length']:,}자")
    output.append(f"  • 요약 길이: {summary_result['summary_length']:,}자")
    output.append(f"  • 압축률: {((1 - summary_result['summary_length'] / summary_result['original_length']) * 100):.1f}%")
    output.append(f"  • 문장 수: {summary_result['sentence_count']}개 → {summary_result['selected_sentences']}개")
    
    return "\n".join(output) 