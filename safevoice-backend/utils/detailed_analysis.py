from nltk.tokenize import sent_tokenize
from utils.abuse_detection import detect_abuse
from utils.emotion_detection import detect_emotions

def analyze_sentences(transcript):
    sentences = sent_tokenize(transcript)
    results = []

    for sentence in sentences:
        abuse = detect_abuse(sentence)
        emotions = detect_emotions(sentence)
        results.append({
            "sentence": sentence,
            "abuse": abuse,
            "emotions": emotions
        })

    return results
