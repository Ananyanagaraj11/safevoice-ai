from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

app = Flask(__name__)

SENDER_EMAIL = "your.email@gmail.com"
SENDER_PASSWORD = "cpnc mqao cnqz alfe" 

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    recipient_email = data.get('recipient')
    subject = data.get('subject', 'SafeVoice Report')
    body = data.get('body', 'Please find the attached SafeVoice report.')
    pdf_data = data.get('pdf_base64')

    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Add attachment (PDF in base64 format)
        if pdf_data:
            import base64
            pdf_content = base64.b64decode(pdf_data)
            attachment = MIMEApplication(pdf_content, _subtype='pdf')
            attachment.add_header('Content-Disposition', 'attachment', filename="SafeVoice_Report.pdf")
            msg.attach(attachment)

        # Send email via Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        return jsonify({"success": True, "message": "Email sent successfully."})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(port=5001)
