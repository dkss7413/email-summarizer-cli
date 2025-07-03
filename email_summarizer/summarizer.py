# 요약 및 키워드 추출 로직 

import re
import math
from typing import List, Tuple, Dict
from collections import Counter

import numpy as np
import torch
from transformers import (
    pipeline, PreTrainedTokenizerFast, BartForConditionalGeneration
)

# ---------------------------
# 환경 설정 (GPU 자동 감지)
# ---------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------------------
# 언어 감지
# ---------------------------
# 입력 텍스트에서 한글/영문 비율을 기반으로 언어를 감지합니다.
def detect_language(text):
    korean_count = len(re.findall(r'[가-힣]', text))
    english_count = len(re.findall(r'[a-zA-Z]', text))
    if korean_count > english_count and korean_count > 10:
        return 'Korean'
    elif english_count > korean_count and english_count > 10:
        return 'English'
    else:
        return 'Mixed'

# ---------------------------
# 문장 분리
# ---------------------------
# 입력 텍스트를 문장 단위로 분리합니다.
def split_sentences(text):
    sentence_endings = re.compile(r'(?<=[.!?。！？])\s+|\n+')
    return [s.strip() for s in sentence_endings.split(text) if s.strip()]

# ---------------------------
# 키워드 추출
# ---------------------------
# 문장 리스트에서 불용어를 제외한 주요 단어(키워드)를 TF-IDF 방식으로 추출합니다.
def extract_keywords(sentences, top_n=10):
    korean_stopwords = {'있다', '없다', '하다', '되다', '보다', '생각하다', '것', '수', '이', '가', '을', '를', '은', '는', '에', '의', '로', '과', '도'}
    english_stopwords = {'the', 'and', 'is', 'are', 'to', 'in', 'that', 'it', 'with', 'as', 'for', 'on', 'was', 'this'}

    words = []
    for s in sentences:
        korean_words = re.findall(r'[가-힣]{2,}', s)
        english_words = re.findall(r'\b[a-zA-Z]{3,}\b', s.lower())
        korean_words = [w for w in korean_words if w not in korean_stopwords]
        english_words = [w for w in english_words if w not in english_stopwords]
        words.extend(korean_words + english_words)

    if not words:
        return []
    word_counts = Counter(words)
    total_words = sum(word_counts.values())
    tf_idf_scores = {
        word: (count / total_words) * math.log(len(sentences) / (1 + sum(1 for s in sentences if word in s)))
        for word, count in word_counts.items()
    }
    return sorted(tf_idf_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

# ---------------------------
# 감정 분석 (BERT 기반)
# ---------------------------
# 입력 텍스트의 감정(긍정/부정/중립 등)을 분석합니다.
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_sentiment(text):
    # pipeline에서 사용하는 tokenizer 직접 불러오기
    tokenizer = sentiment_analyzer.tokenizer
    max_tokens = 512
    tokens = tokenizer.encode(text, truncation=True, max_length=max_tokens)
    # 토큰을 다시 텍스트로 디코딩
    truncated_text = tokenizer.decode(tokens, skip_special_tokens=True)
    result = sentiment_analyzer(truncated_text)
    label = result[0]['label']
    score = result[0]['score']
    return label, score

# 감정 분석 결과(영문 라벨)를 한글로 변환합니다.
def convert_sentiment_to_korean(label, score):
    sentiment_map = {
        "1 star": "매우 부정적", "2 stars": "부정적",
        "3 stars": "중립적", "4 stars": "긍정적", "5 stars": "매우 긍정적"
    }
    korean_sentiment = sentiment_map.get(label, label)
    confidence_level = "높음" if score >= 0.6 else "보통" if score >= 0.3 else "낮음"
    return korean_sentiment, confidence_level

# ---------------------------
# 요약 수행 (seq2seq)
# ---------------------------
# 입력 텍스트와 언어에 따라 BART/KoBART 모델로 요약을 생성합니다.
def summarize_with_seq2seq(text: str, language: str, max_length=150, min_length=40) -> str:
    if language == "Korean":
        tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
        model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization').to(device)

        input_ids = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True).to(device)
        summary_ids = model.generate(
            input_ids,
            max_length=max_length,
            min_length=min_length,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    elif language == "English":
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0 if torch.cuda.is_available() else -1)
        result = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        summary = result[0]['summary_text']

    else:
        summary = "⚠️ 지원되지 않는 언어입니다. 한국어나 영어로 된 텍스트를 입력해 주세요."

    return summary

# ---------------------------
# 통합 파이프라인
# ---------------------------
# 텍스트를 자동으로 언어 감지, 요약, 감정 분석, 키워드 추출까지 한 번에 처리합니다.
def summarize_system_seq2seq(text: str, max_length: int = None, min_length: int = None) -> Dict:
    if not text or len(text) < 30:
        return {"error": "⚠️ 입력이 너무 짧습니다. 최소한 2~3문장 이상의 텍스트를 입력해 주세요."}

    # 자동 길이 결정 로직
    if max_length is None or min_length is None:
        num_chars = len(text)
        num_sentences = len(split_sentences(text))
        # 긴 뉴스(2000자 이상)는 더 길게 요약
        if num_chars >= 2000:
            auto_max = 250
            auto_min = 100
        elif num_chars < 300 or num_sentences <= 3:
            auto_max = 40
            auto_min = 15
        elif num_chars < 1000 or num_sentences <= 8:
            auto_max = 80
            auto_min = 30
        else:
            auto_max = 150
            auto_min = 50
        if max_length is None:
            max_length = auto_max
        if min_length is None:
            min_length = auto_min

    try:
        language = detect_language(text)
        summary = summarize_with_seq2seq(text, language, max_length=max_length, min_length=min_length)
        # 요약 결과가 1문장 이하일 경우 min_length를 늘려서 한 번 더 시도
        summary_sentences = split_sentences(summary)
        if len(summary_sentences) <= 1 and min_length < 120:
            summary = summarize_with_seq2seq(text, language, max_length=max_length, min_length=120)
            summary_sentences = split_sentences(summary)
        # 감정 분석: 원문 전체와 요약문 모두
        sentiment_label_full, sentiment_score_full = analyze_sentiment(text)
        sentiment_label_sum, sentiment_score_sum = analyze_sentiment(summary)
        keywords = extract_keywords(split_sentences(text), top_n=10)

        return {
            "summary": summary,
            "keywords": keywords,
            "sentiment_full": (sentiment_label_full, sentiment_score_full),
            "sentiment_summary": (sentiment_label_sum, sentiment_score_sum),
            "original_length": len(text),
            "summary_length": len(summary),
            "detected_language": language,
            "summary_sentence_count": len(summary_sentences)
        }

    except Exception as e:
        return {"error": f"🚫 오류 발생: {str(e)}"}

# ---------------------------
# 결과 출력
# ---------------------------
# 요약 결과(딕셔너리)를 보기 좋은 문자열로 포맷팅합니다.
def format_seq2seq_summary(summary_result: Dict) -> str:
    if "error" in summary_result:
        return summary_result["error"]

    output = []
    output.append("📝 문맥 기반 요약 결과:")
    output.append("")
    output.append(summary_result["summary"])
    output.append("")

    output.append(f"🌐 언어 감지: {summary_result['detected_language']}")
    # 감정 분석(요약) → 감정 분석 으로 텍스트 변경
    label_sum, score_sum = summary_result["sentiment_summary"]
    korean_sentiment_sum, confidence_level_sum = convert_sentiment_to_korean(label_sum, score_sum)
    output.append(f"😊 감정 분석: {korean_sentiment_sum} (신뢰도: {confidence_level_sum})")
    output.append("")
    output.append("📊 통계:")
    output.append(f"  • 원본 길이: {summary_result['original_length']:,}자")
    output.append(f"  • 요약 길이: {summary_result['summary_length']:,}자")
    output.append(f"  • 요약 문장 수: {summary_result['summary_sentence_count']}문장")

    if summary_result["keywords"]:
        output.append("")
        output.append("🔑 주요 키워드:")
        output.append(", ".join([kw for kw, _ in summary_result["keywords"]]))

    return '\n'.join(output)

# 문서 유형 감지
def detect_text_type(text: str) -> str:
    lines = text.strip().split('\n')
    if any(re.search(r'(보낸[ ]?사람|받는[ ]?사람|제목|from|to|subject):', line.lower()) for line in lines[:5]):
        return 'email'
    return 'general'

# 유형별 요약 전략
def get_summary_strategy(text_type: str) -> Dict:
    strategy = {
        'email': {
            'top_n': 4,
            'diversity': 0.6,
            'redundancy_threshold': 0.8,
            'preprocess': True
        },
        'general': {
            'top_n': 5,
            'diversity': 0.7,
            'redundancy_threshold': 0.85,
            'preprocess': False
        }
    }
    return strategy.get(text_type, strategy['general'])

# MMR 요약
def mmr(doc_embedding, sentence_embeddings, sentences, top_n=5, diversity=0.7, redundancy_threshold=0.85):
    selected = []
    selected_idx = []
    candidate_idx = list(range(len(sentences)))

    while len(selected) < top_n and candidate_idx:
        if not selected:
            sim_to_doc = cosine_similarity(sentence_embeddings, [doc_embedding]).reshape(-1)
            first_idx = int(np.argmax(sim_to_doc))
            selected.append(sentences[first_idx])
            selected_idx.append(first_idx)
            candidate_idx.remove(first_idx)
        else:
            mmr_scores = []
            for idx in candidate_idx:
                sim_to_doc = cosine_similarity([sentence_embeddings[idx]], [doc_embedding])[0][0]
                sim_to_selected = max(
                    cosine_similarity([sentence_embeddings[idx]], [sentence_embeddings[s]])[0][0]
                    for s in selected_idx
                )
                if sim_to_selected > redundancy_threshold:
                    continue
                score = diversity * sim_to_doc - (1 - diversity) * sim_to_selected
                mmr_scores.append((score, idx))

            if not mmr_scores:
                break
            mmr_scores.sort(reverse=True)
            best_idx = mmr_scores[0][1]
            selected.append(sentences[best_idx])
            selected_idx.append(best_idx)
            candidate_idx.remove(best_idx)

    ordered = sorted(zip(selected_idx, selected), key=lambda x: x[0])
    return [s for _, s in ordered]

# 키워드 강조
def highlight_keywords(text, keywords):
    highlighted_text = text
    for keyword, _ in keywords:
        if not keyword.strip():
            continue
        pattern = re.compile(rf'(?<![\w가-힣]){re.escape(keyword)}(?![\w가-힣])', re.IGNORECASE)
        highlighted_text = pattern.sub(f"\033[1;36m{keyword}\033[0m", highlighted_text)
    return highlighted_text

# 요약 파이프라인
def summarize_system(text: str, highlight: bool = True):
    if not text or len(text) < 30:
        return "⚠️ 입력이 너무 짧습니다. 최소한 2~3문장 이상의 텍스트를 입력해 주세요."

    try:
        text_type = detect_text_type(text)
        strategy = get_summary_strategy(text_type)

        sentences = split_sentences(text)
        if len(sentences) < 3:
            raise ValueError("문장이 너무 적습니다.")

        language = detect_language(text)
        sentence_embeddings = embedding_model.encode(sentences)
        doc_embedding = np.mean(sentence_embeddings, axis=0)

        summary_sentences = mmr(
            doc_embedding=doc_embedding,
            sentence_embeddings=sentence_embeddings,
            sentences=sentences,
            top_n=strategy['top_n'],
            diversity=strategy['diversity'],
            redundancy_threshold=strategy['redundancy_threshold']
        )
        summary = ' '.join(summary_sentences)

        keywords = extract_keywords(sentences, top_n=10)
        sentiment_label, sentiment_score = analyze_sentiment(summary)
        summary_highlighted = highlight_keywords(summary, keywords) if highlight else summary

        return {
            "summary": summary_highlighted,
            "keywords": keywords,
            "sentiment": (sentiment_label, sentiment_score),
            "original_length": len(text),
            "summary_length": len(summary),
            "sentence_count": len(sentences),
            "selected_sentences": len(summary_sentences),
            "detected_language": language,
            "text_type": text_type
        }

    except Exception as e:
        print("🚫 오류 발생:", e)
        return None

# 출력 포맷
def format_summary_output(summary_result: Dict) -> str:
    output = []
    output.append("📝 요약 결과:")
    output.append("")

    summary_text = summary_result["summary"]
    lines = []

    if summary_result.get("text_type") == "email":
        header_patterns = [
            r'(보내는 사람\s*:\s*[^\s]+@[^\s]+)',
            r'(받는 사람\s*:\s*[^\s]+@[^\s]+)',
            r'(참조\s*:\s*[^\s]+@[^\s]+)',
            r'(제목\s*:\s*.+)'
        ]
        greeting_pattern = r'(안녕하세요[.!?\s]*)'
        rest = summary_text
        for pat in header_patterns:
            m = re.search(pat, rest)
            if m:
                lines.append(m.group(1).strip())
                rest = rest.replace(m.group(1), '').strip()
        m = re.search(greeting_pattern, rest)
        if m:
            lines.append(m.group(1).strip())
            rest = rest.replace(m.group(1), '').strip()
        sentences = re.split(r'(?<=[.!?。！？])\s+', rest)
        lines += [s.strip() for s in sentences if s.strip()]
    else:
        lines = re.split(r'(?<=[.!?。！？])\s+', summary_text)

    output.append('\n'.join(lines))
    output.append("")
    output.append(f"📄 문서 유형: {summary_result['text_type'].capitalize()}")
    output.append(f"🌐 언어 감지: {summary_result['detected_language']}")
    label, score = summary_result["sentiment"]
    korean_sentiment, confidence_level = convert_sentiment_to_korean(label, score)
    output.append(f"😊 감정 분석: {korean_sentiment} (신뢰도: {confidence_level})")
    output.append("")
    output.append("📊 통계:")
    output.append(f"  • 원본 길이: {summary_result['original_length']:,}자")
    output.append(f"  • 요약 길이: {summary_result['summary_length']:,}자")
    output.append(f"  • 문장 수: {summary_result['sentence_count']}개 → {summary_result['selected_sentences']}개")
    return '\n'.join(output) 