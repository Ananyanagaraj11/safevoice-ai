from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.audio_to_text import transcribe_audio
from utils.analysis_utils import analyze_sentences, get_top_emotions
from utils.abuse_detection import detect_abuse

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files["audio"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        transcript = transcribe_audio(file)
        sentence_analysis = analyze_sentences(transcript)
        abuse_overall = detect_abuse(transcript)
        top_emotion, emotion_all = get_top_emotions(sentence_analysis)

        return jsonify({
            "transcript": transcript,
            "detailed_analysis": sentence_analysis,
            "abuse": abuse_overall,
            "emotions": {
                "top": top_emotion,
                "all": emotion_all
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
