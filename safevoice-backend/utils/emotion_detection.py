from transformers import pipeline

emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

def detect_emotions(text):
    predictions = emotion_classifier(text)[0]
    emotions = [
        {"label": pred["label"].lower(), "score": round(pred["score"], 3)}
        for pred in sorted(predictions, key=lambda x: x["score"], reverse=True)
    ]
    return emotions
