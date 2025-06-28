from transformers import pipeline

abuse_classifier = pipeline("text-classification", model="unitary/toxic-bert", top_k=None)

def detect_abuse(text):
    predictions = abuse_classifier(text)[0]
    toxic_score = next((p["score"] for p in predictions if p["label"].lower() == "toxic"), 0)
    return {"label": "toxic", "score": round(toxic_score, 3)}
