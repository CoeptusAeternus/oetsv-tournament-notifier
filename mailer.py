import logging
import os
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .models.mail import Mail, NewTournamentMail, NennschlussMail

SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

RECIPIENTS = os.environ.get('RECIPIENTS').split(',')
RECIPIENTS = map(lambda x: x.strip(), RECIPIENTS)

if not SMTP_SERVER or not SMTP_PORT or not SMTP_USERNAME or not SMTP_PASSWORD:
    raise ValueError("SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD must be set")

def send_email(mail: Mail):
    
    subject, body, sender = mail.format_for_sending(RECIPIENTS)
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))    
    
    logging.debug(f"attempting mail server login on {SMTP_SERVER}:{SMTP_PORT}")
    try:
        with SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            logging.debug(f"attempting mail server login with {SMTP_USERNAME}")
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            
            logging.debug(f"attempting to send email to {RECIPIENTS}")
            for recipient in RECIPIENTS:
                msg['To'] = recipient
                smtp.send_message(msg.as_string)
                
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return
