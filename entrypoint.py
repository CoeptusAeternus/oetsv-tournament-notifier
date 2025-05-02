#!/usr/bin/env python3
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Setup")
logger.info("Starting Setup")

#check all necessary environment variables are set
REQUIRED_ENV_DICT ={
    "SMTP_SERVER": os.getenv("SMTP_SERVER", None),
    "SMTP_PORT": os.getenv("SMTP_PORT", None),
    "SMTP_USERNAME": os.getenv("SMTP_USERNAME", None),
    "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD", None),
    "RECIPIENTS": os.getenv("RECIPIENTS", None),
    "NOTIFIED_PATH": os.getenv("NOTIFIED_PATH", None),
}

missing_env_vars = [key for key, value in REQUIRED_ENV_DICT.items() if value is None]

if missing_env_vars:
    logger.error(f"Missing environment variables: {missing_env_vars}")
    exit(1)

# setup notified file

NOTIFIED_FILE = os.getenv("NOTIFIED_PATH")

if not os.path.exists(NOTIFIED_FILE):
    logger.info(f"Creating file {NOTIFIED_FILE}")
    with open(NOTIFIED_FILE, "w") as f:
        f.write("")
else:
    logger.info(f"File {NOTIFIED_FILE} already exists")
    logger.warning("File will be overwritten")
    os.remove(NOTIFIED_FILE)
    with open(NOTIFIED_FILE, "w") as f:
        f.write("")
    
from api_service import get_tournaments

tournaments = get_tournaments()
if not tournaments:
    logger.warning("No tournaments found")

for t in tournaments:
    with open(NOTIFIED_FILE, "a") as f:
        f.write(f"{t.id}\n")

logger.info(f"Added {len(tournaments)} tournaments to {NOTIFIED_FILE}")

logger.info("All necessary environment variables are set - proceeding with Startup")
    