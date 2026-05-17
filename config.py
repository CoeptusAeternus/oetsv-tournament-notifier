"""Configuration - Load environment variables."""

import os
from pathlib import Path

# SMTP Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT_RAW = os.getenv("SMTP_PORT")
SMTP_PORT = int(SMTP_PORT_RAW) if SMTP_PORT_RAW else None
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Email Recipients
RECIPIENTS = [email.strip() for email in os.getenv("RECIPIENTS", "").split(",") if email.strip()]

# API Configuration
API_URL = os.getenv("API_URL")

# File Configuration
NOTIFIED_PATH = Path(os.getenv("NOTIFIED_PATH", "./notified.txt"))

# Notifier Configuration
DAYS_BEFORE_TOURNAMENT = int(os.getenv("DAYS_BEFORE_TOURNAMENT", 13))

# Validate required env vars
missing = []
for var, value in {
    "SMTP_SERVER": SMTP_SERVER,
    "SMTP_PORT": SMTP_PORT,
    "SMTP_USERNAME": SMTP_USERNAME,
    "SMTP_PASSWORD": SMTP_PASSWORD,
    "RECIPIENTS": RECIPIENTS,
    "API_URL": API_URL,
}.items():
    if not value:
        missing.append(var)

if missing:
    raise ValueError(f"Missing required environment variables: {missing}")
