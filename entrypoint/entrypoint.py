#!/usr/bin/env python3
import os
import logging

#check all necessary environment variables are set
REQUIRED_ENV_DICT ={
    "SAMPLE_ENV": os.environ.get("SAMPLE_ENV", None),
}

missing_env_vars = [key for key, value in REQUIRED_ENV_DICT.items() if value is None]

if missing_env_vars:
    logging.error(f"Missing environment variables: {missing_env_vars}")
    exit(1)
else:
    logging.info("All necessary environment variables are set - proceeding with Startup")
    