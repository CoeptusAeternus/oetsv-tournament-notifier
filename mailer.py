import logging
import os
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

from models.mail import Mail

SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

RECIPIENTS = os.environ.get('RECIPIENTS').split(',')
RECIPIENTS = list(map(lambda x: x.strip(), RECIPIENTS))

if not SMTP_SERVER or not SMTP_PORT or not SMTP_USERNAME or not SMTP_PASSWORD:
    raise ValueError("SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD must be set")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def send_email(mail: Mail):
    
    subject, body, sender = mail.format_for_sending(RECIPIENTS)
    
    msg = MIMEMultipart()
    msg['From'] = formataddr((sender, SMTP_USERNAME))
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))    
    
    logger.debug(type(mail))
    
    logger.debug(f"attempting mail server login on {SMTP_SERVER}:{SMTP_PORT}")
    try:
        with SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            logger.debug(f"attempting mail server login with {SMTP_USERNAME}")
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            logger.debug("login successfull")
            
            for recipient in RECIPIENTS:
                logger.debug(f"attempting to send email to {recipient}")
                msg['To'] = recipient
                smtp.send_message(msg)
                logger.info("sent {} to {} for tid {}".format(type(mail), recipient, mail.tournament.id) )
                
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return
