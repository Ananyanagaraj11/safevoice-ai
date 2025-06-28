from transformers import pipeline

# Load the emotion detection model with top_k=None to get all scores
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)
abuse_model = pipeline("text-classification", model="unitary/toxic-bert", top_k=None)

def detect_emotions(text):
    try:
        result = emotion_model(text)
        if isinstance(result, list) and isinstance(result[0], list):
            result = result[0]
        return sorted(result, key=lambda x: x['score'], reverse=True)
    except Exception as e:
        return [{"label": "unknown", "score": 0.0, "error": str(e)}]

def detect_abuse(text):
    try:
        results = abuse_model(text)
        if isinstance(results, list) and isinstance(results[0], list):
            results = results[0]
        abusive = [res for res in results if res['score'] > 0.5]
        return abusive
    except Exception as e:
        return [{"label": "unknown", "score": 0.0, "error": str(e)}]

