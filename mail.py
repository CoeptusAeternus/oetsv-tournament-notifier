"""Email sending."""

import logging
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from models import Mail

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def send_email(mail: Mail, smtp_server: str, smtp_port: int, smtp_user: str, smtp_pass: str, recipients: list[str]) -> None:
    """Send email."""
    subject = mail.get_subject()
    body = mail.get_body()
    sender = mail.get_sender()
    
    msg = MIMEMultipart()
    msg["From"] = formataddr((sender, smtp_user))
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))
    
    with SMTP(smtp_server, smtp_port, timeout=10) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(smtp_user, smtp_pass)
        
        for recipient in recipients:
            msg["To"] = recipient
            try:
                smtp.send_message(msg)
            except Exception as e:
                logging.error(f"Failed to send email to {recipient}: {e}")
    
