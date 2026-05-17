#!/usr/bin/env python3

import os
from typing import List
import logging

from api_service import get_tournaments
from mailer import send_email
from models.mail import NewTournamentMail
from models.tournamet_models import ShortTournament

STARTUP_RUN = True

NOTIFIED_FILE = os.getenv("NOTIFIED_PATH")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NewTournamentNotifier")
logger.setLevel(logging.INFO)

def get_notified_tournaments() -> List[int]:
    assert os.path.exists(NOTIFIED_FILE), f"File {NOTIFIED_FILE} does not exist"
    try:
        with open(NOTIFIED_FILE, "r") as f:
            logger.debug(f"Reading notified tournaments from {NOTIFIED_FILE}")
            return [int(line.strip()) for line in f.readlines()]
    except Exception as e:
        logger.error(f"Error reading notified tournaments from {NOTIFIED_FILE}")
        logger.error(e)
        return []

def add_to_notified_file(tournament: ShortTournament) -> None:
    try:
        logger.debug(f"Adding tournament {tournament.id} to {NOTIFIED_FILE}")
        with open(NOTIFIED_FILE, "a") as f:
            f.write(f"{tournament.id}\n")
    except Exception as e:
        logger.error(f"Error adding tournament {tournament.id} to {NOTIFIED_FILE}")
        logger.error(e)

    
def main():
    current_tournaments = get_tournaments()
    
    notified_tournaments = get_notified_tournaments()
    new_tournaments = filter(lambda t: t.id not in notified_tournaments, current_tournaments)
    
    for tournament in new_tournaments:
        logger.info(f"Creating mail for tournament {tournament.id}")
        mail = NewTournamentMail(tournament = tournament)
        add_to_notified_file(tournament)
        send_email(mail)



if __name__ == "__main__":
    main()
