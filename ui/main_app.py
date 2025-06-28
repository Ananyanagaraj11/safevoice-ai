import streamlit as st
from app.abuse_detection import detect_abuse

st.title("SAFEVOICE: Verbal Abuse Detector 🔊🛡️")

text = st.text_area("Paste conversation or transcript here:")

if st.button("Analyze"):
    if text:
        result = detect_abuse(text)
        st.write("Risk:", result[0]["label"])
        st.write("Confidence:", round(result[0]["score"] * 100, 2), "%")
    else:
        st.warning("Please enter text.")
