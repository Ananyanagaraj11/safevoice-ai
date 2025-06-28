"""
Generate a polished PDF report for SafeVoice.

Features
--------
• Full transcript
• Summary (dominant emotion + abuse categories)
• Sentence-level table of emotions & abuse
• Inline bar-chart image (optional)
• Emergency safety numbers

Usage
-----
from utils.report_generator import generate_pdf
pdf_path = generate_pdf(
        transcript,
        sentence_results,   # list from detailed_analysis
        summary_dict,       # {"dominant_emotion": str, "abuse_detected": bool, "abuse_labels": [...] }
        chart_path="emotion_chart.png",  # optional
        output_path="SafeVoice_Report.pdf"
)
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

EMERGENCY_CONTACTS = [
    "🇺🇸 USA – 911",
    "🇮🇳 India – 100 / 112",
    "🇬🇧 UK – 999",
    "🇨🇦 Canada – 911",
    "🇦🇺 Australia – 000",
    "🇳🇿 New Zealand – 111",
    "🇿🇦 South Africa – 10111",
    "🇫🇷 France – 112",
    "🇩🇪 Germany – 110 / 112",
    "🇪🇸 Spain – 112",
    "🇮🇹 Italy – 112",
    "🇯🇵 Japan – 110 (Police), 119 (Ambulance/Fire)",
    "🇨🇳 China – 110 (Police), 120 (Ambulance)",
    "🇰🇷 South Korea – 112 (Police), 119 (Fire/Medical)",
    "🇧🇷 Brazil – 190 (Police), 192 (Ambulance)",
    "🇲🇽 Mexico – 911",
    "🇷🇺 Russia – 112",
    "🇸🇬 Singapore – 999 (Police), 995 (Ambulance)",
    "🇲🇾 Malaysia – 999 / 112",
    "🇵🇭 Philippines – 911",
]



def _sentence_table(rows):
    """Return a styled ReportLab Table for sentence-level results."""
    data = [["Sentence", "Top Emotions", "Abuse?"]]
    for row in rows:
        emotions = ", ".join(
            f"{e['label']} ({e['score']:.2f})" for e in row["emotions"]
        )
        if row["abuse"]["is_abusive"]:
            abuse_txt = "Yes – " + ", ".join(
                c["label"] for c in row["abuse"]["categories"]
            )
        else:
            abuse_txt = "No"
        data.append([row["sentence"], emotions, abuse_txt])

    tbl = Table(data, colWidths=[260, 150, 120])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ]
        )
    )
    return tbl


def generate_pdf(
    transcript: str,
    sentence_results: list,
    summary: dict,
    chart_path: str | None = None,
    output_path: str = "SafeVoice_Report.pdf",
):
    """Create the PDF and return its path."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=30,
        title="SafeVoice Report",
    )
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(
        Paragraph("SafeVoice – Emotional & Abuse Analysis Report", styles["Title"])
    )
    story.append(
        Paragraph(datetime.now().strftime("Generated on %Y-%m-%d %H:%M"), styles["Normal"])
    )
    story.append(Spacer(1, 18))

    # Transcript
    story.append(Paragraph("Transcript", styles["Heading2"]))
    story.append(Paragraph(transcript.replace("\n", "<br/>"), styles["BodyText"]))
    story.append(Spacer(1, 18))

    # Summary
    story.append(Paragraph("Summary", styles["Heading2"]))
    summ_html = (
        f"Dominant emotion: <b>{summary['dominant_emotion']}</b><br/>"
        + (
            f"⚠️ Abuse detected – {', '.join(summary['abuse_labels'])}"
            if summary["abuse_detected"]
            else "No significant abuse detected."
        )
    )
    story.append(Paragraph(summ_html, styles["BodyText"]))
    story.append(Spacer(1, 18))

    # Sentence-level table
    story.append(Paragraph("Sentence-level Analysis", styles["Heading2"]))
    story.append(_sentence_table(sentence_results))
    story.append(Spacer(1, 18))

    # Chart
    if chart_path and os.path.isfile(chart_path):
        story.append(Paragraph("Emotion Breakdown Chart", styles["Heading2"]))
        story.append(Image(chart_path, width=440, preserveAspectRatio=True))
        story.append(Spacer(1, 18))

    # Emergency numbers
    story.append(Paragraph("Emergency Numbers", styles["Heading2"]))
    story.extend(
        [Paragraph(f"• {num}", styles["Normal"]) for num in EMERGENCY_CONTACTS]
    )

    doc.build(story)
    return output_path
