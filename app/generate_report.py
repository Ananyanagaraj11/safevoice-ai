import json
import os
from fpdf import FPDF
import matplotlib.pyplot as plt
from collections import Counter

# ========= CONFIG =========
INPUT_FILE = "../outputs/detailed_report.json"
PDF_FILE = "../outputs/safevoice_report.pdf"
CHART_FILE = "../outputs/emotion_chart.png"

# ========= LOAD REPORT DATA =========
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# ========= EMOTION CHART =========
def generate_emotion_chart():
    emotions = [entry["emotion"]["label"] for entry in data["analysis"]]
    counts = Counter(emotions)

    plt.figure(figsize=(6, 4))
    plt.bar(counts.keys(), counts.values())
    plt.title("Emotion Frequency in Transcript")
    plt.xlabel("Emotion")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(CHART_FILE)
    plt.close()
    print("📊 Emotion chart saved to", CHART_FILE)

# ========= PDF GENERATION =========
def generate_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "SafeVoice Report", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Audio File: {data['audio_file']}", ln=True)
    pdf.multi_cell(0, 10, f"\nTranscript:\n{data['transcript']}")

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Detailed Analysis", ln=True)

    pdf.set_font("Arial", "", 11)
    for idx, entry in enumerate(data["analysis"], 1):
        pdf.multi_cell(0, 8, f"{idx}. {entry['sentence']}")
        pdf.cell(0, 8, f"   -> Emotion: {entry['emotion']['label']} ({entry['emotion']['confidence']})", ln=True)
        pdf.cell(0, 8, f"   -> Abuse: {entry['abuse']['label']} ({entry['abuse']['confidence']})", ln=True)
        pdf.ln(1)

    pdf.image(CHART_FILE, x=10, y=pdf.get_y() + 5, w=180)
    pdf.output(PDF_FILE)
    print("📄 PDF report saved to", PDF_FILE)

# ========= MAIN RUN =========
if __name__ == "__main__":
    generate_emotion_chart()
    generate_pdf_report()
