import whisper
import os
import torch

# Load Whisper model
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device set to use {DEVICE}")
whisper_model = whisper.load_model("base", device=DEVICE)

def transcribe_audio(file_path):
    """
    Transcribes an audio file to text using Whisper.
    Accepts .wav, .mp3, .m4a, etc.
    Returns transcribed text.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found at: {file_path}")

    print("Transcribing audio...")
    result = whisper_model.transcribe(file_path)
    text = result.get("text", "").strip()

    if not text:
        raise ValueError("Transcription failed or returned empty text.")

    return text
