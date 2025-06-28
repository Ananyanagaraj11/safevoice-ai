import smtplib
from email.message import EmailMessage

def send_email(to_email, pdf_path):
    msg = EmailMessage()
    msg["Subject"] = "SafeVoice Report"
    msg["From"] = "safevoice.alerts@gmail.com"
    msg["To"] = to_email
    msg.set_content("Please find the SafeVoice report attached.")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="safevoice_report.pdf")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("safevoice.alerts@gmail.com", "your-app-password")  # Use app password or dummy for now
        smtp.send_message(msg)
