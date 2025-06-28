import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

def generate_emotion_chart(emotions, chart_path):
    labels = [e['label'] for e in emotions]
    scores = [e['score'] for e in emotions]
    plt.figure(figsize=(6, 4))
    plt.bar(labels, scores)
    plt.title("Detected Emotions")
    plt.ylabel("Confidence")
    plt.savefig(chart_path)
    plt.close()

def create_pdf_report(transcript, emotions, chart_path, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, "SafeVoice Analysis Report")
    c.setFont("Helvetica", 10)
    c.drawString(50, 730, "Transcript:")
    text = c.beginText(50, 710)
    text.textLines(transcript)
    c.drawText(text)
    if chart_path:
        c.drawImage(ImageReader(chart_path), 50, 400, width=500, height=200)
    c.drawString(50, 360, "Detected Emotions:")
    y = 340
    for e in emotions:
        c.drawString(60, y, f"{e['label']}: {round(e['score'], 2)}")
        y -= 15
    c.drawString(50, y - 20, "Emergency Numbers:")
    c.drawString(60, y - 40, "• USA: 911")
    c.drawString(60, y - 55, "• India: 100")
    c.save()
