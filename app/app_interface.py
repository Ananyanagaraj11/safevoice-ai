import streamlit as st
import whisper
from transformers import pipeline
import soundfile as sf
import smtplib
from email.message import EmailMessage
import os
from utils import generate_emotion_chart, create_pdf_report

# Models
asr = whisper.load_model("base")
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=5)

# Paths
CHART_FILE = "outputs/emotion_chart.png"
PDF_FILE = "outputs/safevoice_report.pdf"
os.makedirs("outputs", exist_ok=True)

st.title("🎙️ SafeVoice – Record. Analyze. Act.")
st.markdown("Tap to record or upload a voice message. Get emotion and abuse insights in a downloadable PDF report.")

# Audio input
audio_file = None
st.markdown("📤 Upload voice message (WAV/MP3)")
st.write("or")
if st.button("🎤 Start Recording"):
    st.info("Recording started... Please stop manually after speaking.")
    st.stop()  # Let user record separately via browser tool like Vocaroo or phone

uploaded = st.file_uploader("Upload your voice file here", type=["wav", "mp3"])
if uploaded:
    with open("temp.wav", "wb") as f:
        f.write(uploaded.read())
    audio_path = "temp.wav"

    st.audio(audio_path)

    # Transcription
    with st.spinner("Transcribing..."):
        transcript = asr.transcribe(audio_path)["text"].strip()
        st.success("Transcription complete!")
        st.markdown(f"**Transcript:** {transcript}")

    # Emotion detection
    with st.spinner("Analyzing emotions..."):
        emotions = emotion_model(transcript)[0]
        st.success("Emotion analysis complete!")

    # Chart & PDF
    generate_emotion_chart(emotions, CHART_FILE)
    create_pdf_report(transcript, emotions, CHART_FILE, PDF_FILE)

    st.image(CHART_FILE, caption="Emotion Chart", use_column_width=True)
    st.download_button("📄 Download Report", data=open(PDF_FILE, "rb"), file_name="safevoice_report.pdf")

    # Emergency info
    st.markdown("### 📞 Emergency Contact Numbers")
    st.markdown("• **USA**: 911  \n• **India**: 100")

    # Email option
    st.markdown("### 📧 Send to Trusted Person")
    trusted_email = st.text_input("Enter their email")
    if st.button("Send Report"):
        if trusted_email:
            msg = EmailMessage()
            msg["Subject"] = "SafeVoice Report"
            msg["From"] = "safevoice.alerts@gmail.com"
            msg["To"] = trusted_email
            msg.set_content("Attached is the SafeVoice analysis report.")
            with open(PDF_FILE, "rb") as f:
                msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="safevoice_report.pdf")
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login("safevoice.alerts@gmail.com", "your-app-password")
                    smtp.send_message(msg)
                st.success("Email sent!")
            except Exception as e:
                st.error(f"Email failed: {e}")
        else:
            st.warning("Please enter an email.")
