from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

def create_pdf(transcript, analysis, chart_path, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "SafeVoice Emotional & Abuse Analysis Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Transcript:")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 100, transcript[:300] + "...")

    y = height - 150
    for a in analysis:
        if y < 100:
            c.showPage()
            y = height - 50
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"{a['sentence']} → Emotion: {a['emotion']['label']}, Abuse: {a['abuse']['label']}")
        y -= 20

    c.drawImage(ImageReader(chart_path), 50, 100, width=500, preserveAspectRatio=True)
    c.save()
