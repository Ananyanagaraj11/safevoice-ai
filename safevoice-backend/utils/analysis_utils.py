"""
Emotion + abuse utilities
-------------------------
• analyze_sentences(text)  → sentence-level list
• get_top_emotions(list)   → (top_emotion_dict, all_emotions_dict)
"""

import nltk
from collections import defaultdict, Counter
from transformers import pipeline

# ──────────────────────────────────────────────────────────────────────────
# 1.  MODELS (load once at import time)
# ──────────────────────────────────────────────────────────────────────────
#   Emotion model → returns top-k scores for 7 basic emotions
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=7,                # we’ll slice later
    truncation=True
)

#   Abuse detector (your existing util)
from utils.abuse_detection import detect_abuse

# ──────────────────────────────────────────────────────────────────────────
# 2.  Sentence tokenizer – make sure punkt is present
# ──────────────────────────────────────────────────────────────────────────
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)
from nltk.tokenize import sent_tokenize


# ──────────────────────────────────────────────────────────────────────────
# 3.  Sentence-level analysis
# ──────────────────────────────────────────────────────────────────────────
def analyze_sentences(transcript: str):
    """
    → List[ { sentence, emotions:[{label,score}], abuse:{label,score} } ]
    Scores are rounded to 2 dp.
    """
    sentences = [s.strip() for s in sent_tokenize(transcript) if s.strip()]
    results   = []

    for sent in sentences:
        # Emotion scores (we keep top-3 only for UI clarity)
        e_scores = emotion_model(sent)[0]            # list[dict]
        e_top3   = sorted(e_scores, key=lambda x: x["score"], reverse=True)[:3]
        for e in e_top3:
            e["score"] = round(e["score"], 2)

        results.append({
            "sentence": sent,
            "emotions": e_top3,
            "abuse":    detect_abuse(sent)           # already rounded inside util
        })
    return results


# ──────────────────────────────────────────────────────────────────────────
# 4.  Aggregate helpers for the whole transcript
# ──────────────────────────────────────────────────────────────────────────
def get_top_emotions(sentence_analysis):
    """
    sentence_analysis  ← output of analyze_sentences()
    returns (top_emotion_dict, all_emotions_percent_dict)
    """
    # Accumulate raw scores
    bucket = Counter()
    for s in sentence_analysis:
        for e in s["emotions"]:
            bucket[e["label"]] += e["score"]

    total = sum(bucket.values()) or 1.0
    all_emotions_percent = {
        lbl: round(v / total * 100, 1) for lbl, v in bucket.items()
    }

    top_lbl, top_val = max(bucket.items(), key=lambda kv: kv[1])
    top_emotion = {"label": top_lbl, "score": round(top_val / total, 3)}

    return top_emotion, all_emotions_percent
