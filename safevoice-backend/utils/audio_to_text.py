import tempfile
import whisper

model = whisper.load_model("base")

def transcribe_audio(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        file.save(temp_audio.name)  # 'file' is a werkzeug FileStorage object
        temp_audio_path = temp_audio.name

    result = model.transcribe(temp_audio_path)
    return result["text"]
