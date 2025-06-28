from abuse_detection import detect_abuse
from transformers import pipeline

# Load emotion detection pipeline
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=3  # Return top 3 emotions per sentence
)

def analyze_sentences(transcript):
    """
    Performs sentence-level emotion and abuse analysis.
    Returns a list of dicts per sentence with:
    - sentence
    - emotion (top 3)
    - abuse result
    """
    import nltk
    nltk.download('punkt', quiet=True)
    from nltk.tokenize import sent_tokenize

    sentences = sent_tokenize(transcript)
    results = []

    for sent in sentences:
        emotion_scores = emotion_model(sent)
        abuse_result = detect_abuse(sent)

        results.append({
            "sentence": sent,
            "emotions": [
                {"label": e["label"], "score": round(e["score"], 2)}
                for e in emotion_scores
            ],
            "abuse": abuse_result
        })

    return results
