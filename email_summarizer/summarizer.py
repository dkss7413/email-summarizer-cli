# 요약 및 키워드 추출 로직 

import re
import numpy as np
from typing import List, Tuple, Dict
from collections import Counter
import math
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

# 모델 로딩
print("모델 로딩 중...")
embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
print("모델 로딩 완료!")

# 문장 분리 (한글/영문/혼합 모두 자연스럽게)
def split_sentences(text):
    # 한글: 마침표, 물음표, 느낌표, 줄바꿈, 영문: .!?\n, 한글: 。！？ 포함
    # 문장 끝에 공백/줄바꿈이 올 수 있음
    sentence_endings = re.compile(r'(?<=[.!?。！？])\s+|\n+')
    sentences = sentence_endings.split(text)
    return [s.strip() for s in sentences if s.strip()]

# 언어 감지
def detect_language(text):
    korean_count = len(re.findall(r'[가-힣]', text))
    english_count = len(re.findall(r'[a-zA-Z]', text))
    if korean_count > english_count and korean_count > 10:
        return 'Korean'
    elif english_count > korean_count and english_count > 10:
        return 'English'
    else:
        return 'Mixed'

# 키워드 추출 (개선된 TF-IDF)
def extract_keywords(sentences, top_n=10):
    words = []
    for s in sentences:
        words += re.findall(r'\b\w+\b', s.lower())
    word_counts = Counter(words)
    total_words = sum(word_counts.values())
    tf_idf_scores = {}
    for word, count in word_counts.items():
        tf = count / total_words
        idf = math.log(len(sentences) / (1 + sum(1 for s in sentences if word in s.lower())))
        tf_idf_scores[word] = tf * idf
    sorted_keywords = sorted(tf_idf_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_keywords[:top_n]

# MMR 기반 요약 (핵심성 + 다양성)
def mmr(doc_embedding, sentence_embeddings, sentences, top_n=5, diversity=0.7):
    selected = []
    selected_idx = []
    candidate_idx = [i for i in range(len(sentences))]

    while len(selected) < top_n and candidate_idx:
        if not selected:
            # 첫 문장: 가장 중요한 것 선택 (문서 중심과 가장 유사한 것)
            sim_to_doc = cosine_similarity(sentence_embeddings, [doc_embedding]).reshape(-1)
            first_idx = int(np.argmax(sim_to_doc))
            selected.append(sentences[first_idx])
            selected_idx.append(first_idx)
            candidate_idx.remove(first_idx)
        else:
            mmr_scores = []
            for idx in candidate_idx:
                sim_to_doc = cosine_similarity([sentence_embeddings[idx]], [doc_embedding])[0][0]
                sim_to_selected = max(cosine_similarity([sentence_embeddings[idx]], [sentence_embeddings[s]])[0][0] for s in selected_idx)
                score = diversity * sim_to_doc - (1 - diversity) * sim_to_selected
                mmr_scores.append((score, idx))
            mmr_scores.sort(reverse=True)
            best_idx = mmr_scores[0][1]
            selected.append(sentences[best_idx])
            selected_idx.append(best_idx)
            candidate_idx.remove(best_idx)

    # 원문 순서 유지
    ordered = sorted(zip(selected_idx, selected), key=lambda x: x[0])
    return [s for (_, s) in ordered]

# 요약 생성
def generate_summary(text: str, length_option: str = "normal") -> Tuple[str, List[str]]:
    sentences = split_sentences(text)
    if len(sentences) < 3:
        raise ValueError("입력 텍스트가 너무 짧습니다. 최소 3문장 이상 필요합니다.")
    
    embeddings = embedding_model.encode(sentences)
    if length_option == "short":
        n_clusters = min(3, len(sentences))
    elif length_option == "long":
        n_clusters = min(8, len(sentences))
    else:  # normal
        n_clusters = min(5, len(sentences))
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(embeddings)
    
    summary_sentences = []
    for i in range(n_clusters):
        cluster_indices = np.where(kmeans.labels_ == i)[0]
        cluster_embeddings = embeddings[cluster_indices]
        center = kmeans.cluster_centers_[i]
        distances = np.linalg.norm(cluster_embeddings - center, axis=1)
        closest_idx = cluster_indices[np.argmin(distances)]
        summary_sentences.append(sentences[closest_idx])

    summary_sentences.sort(key=lambda x: sentences.index(x))
    summary = ' '.join(summary_sentences)
    return summary, sentences

# 개선된 키워드 강조 (한글/영문 단어 경계)
def highlight_keywords(text, keywords):
    for keyword, _ in keywords:
        if not keyword.strip():
            continue  # 빈 키워드 무시
        # 한글/영문 단어 경계에만 강조
        pattern = re.compile(rf'(?<![\w가-힣]){re.escape(keyword)}(?![\w가-힣])', re.IGNORECASE)
        text = pattern.sub(f"**{keyword}**", text)
    return text

# 감정 분석
def analyze_sentiment(text):
    result = sentiment_analyzer(text)
    label = result[0]['label']
    score = result[0]['score']
    return label, score

# 전체 파이프라인
def summarize_system(text: str, length_option: str = "normal", highlight: bool = True):
    if not text or len(text) < 30:
        return "⚠️ 입력이 너무 짧습니다. 최소한 2~3문장 이상의 텍스트를 입력해 주세요."

    try:
        sentences = split_sentences(text)
        if len(sentences) < 3:
            raise ValueError("문장이 너무 적습니다.")

        language = detect_language(text)

        sentence_embeddings = embedding_model.encode(sentences)
        doc_embedding = np.mean(sentence_embeddings, axis=0)

        # 요약 길이 설정
        if length_option == "short":
            n_sentences = min(3, len(sentences))
        elif length_option == "long":
            n_sentences = min(8, len(sentences))
        else:  # normal
            n_sentences = min(5, len(sentences))

        summary_sentences = mmr(doc_embedding, sentence_embeddings, sentences, top_n=n_sentences)
        summary = ' '.join(summary_sentences)

        keywords = extract_keywords(sentences, top_n=10)
        sentiment_label, sentiment_score = analyze_sentiment(summary)

        if highlight:
            summary_highlighted = highlight_keywords(summary, keywords)
        else:
            summary_highlighted = summary

        return {
            "summary": summary_highlighted,
            "keywords": keywords,
            "sentiment": (sentiment_label, sentiment_score),
            "original_length": len(text),
            "summary_length": len(summary),
            "sentence_count": len(sentences),
            "selected_sentences": len(summary_sentences),
            "detected_language": language
        }
    except Exception as e:
        print("🚫 오류 발생:", e)
        return None

def format_summary_output(summary_result: Dict) -> str:
    output = []
    output.append("📝 요약 결과:")
    output.append("")
    output.append(summary_result["summary"])
    output.append("")
    if summary_result["keywords"]:
        output.append("🔑 주요 키워드:")
        for i, (kw, score) in enumerate(summary_result["keywords"], 1):
            output.append(f"  {i}. {kw} (TF-IDF: {score:.3f})")
        output.append("")
    output.append(f"🌐 언어 감지: {summary_result['detected_language']}")
    label, score = summary_result["sentiment"]
    output.append(f"😊 감정 분석: {label} (신뢰도: {score:.2f})")
    output.append("")
    output.append("📊 통계:")
    output.append(f"  • 원본 길이: {summary_result['original_length']:,}자")
    output.append(f"  • 요약 길이: {summary_result['summary_length']:,}자")
    output.append(f"  • 문장 수: {summary_result['sentence_count']}개 → {summary_result['selected_sentences']}개")
    return '\n'.join(output) 