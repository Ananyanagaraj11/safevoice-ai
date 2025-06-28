from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_pdf_report(transcript, analysis_result):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 50, "SafeVoice AI Report")

    c.setFont("Helvetica", 12)
    c.drawString(40, height - 80, f"Top Emotion: {analysis_result['emotions']['top']['label']} ({round(analysis_result['emotions']['top']['score'] * 100, 1)}%)")
    c.drawString(40, height - 100, f"Abuse Detected: {analysis_result['abuse']['label']} ({round(analysis_result['abuse']['score'] * 100, 1)}%)")

    c.drawString(40, height - 130, "Transcript:")
    text_obj = c.beginText(40, height - 150)
    text_obj.setFont("Helvetica", 10)
    for line in transcript.split('\n'):
        text_obj.textLine(line)
    c.drawText(text_obj)

    y = text_obj.getY() - 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Sentence-Level Analysis:")
    y -= 20

    for sentence in analysis_result["detailed_analysis"]:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(40, y, f"• {sentence['sentence']}")
        y -= 15
        c.setFont("Helvetica", 10)
        c.drawString(60, y, f"Abuse: {sentence['abuse']['label']} ({round(sentence['abuse']['score'] * 100, 1)}%)")
        y -= 15
        emo_summary = ", ".join([f"{e['label']} ({round(e['score'] * 100, 1)}%)" for e in sentence['emotions'][:3]])
        c.drawString(60, y, f"Emotions: {emo_summary}")
        y -= 25
        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
    buffer.seek(0)
    return buffer
