#!/usr/bin/env python3
import os
import logging

#check all necessary environment variables are set
REQUIRED_ENV_DICT ={
    "SMTP_SERVER": os.getenv("SMTP_SERVER", None),
    "SMTP_PORT": os.getenv("SMTP_PORT", None),
    "SMTP_USER": os.getenv("SMTP_USER", None),
    "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD", None),
    "RECIPIENTS": os.getenv("RECIPIENTS", None),
}

missing_env_vars = [key for key, value in REQUIRED_ENV_DICT.items() if value is None]

if missing_env_vars:
    logging.error(f"Missing environment variables: {missing_env_vars}")
    exit(1)
else:
    logging.info("All necessary environment variables are set - proceeding with Startup")
    