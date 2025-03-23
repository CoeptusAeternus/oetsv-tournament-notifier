#!/usr/bin/env python3

import os
import datetime
import logging
from typing import List

from api_service import get_tournaments
from mailer import send_email
from models.tournamet_models import ShortTournament
from models.mail import NennschlussMail

DAYS_BEFORE_TOURNAMENT = os.getenv("DAYS_BEFORE_TOURNAMENT", 13)

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("nennschluss_notifier")
logger.setLevel(logging.DEBUG)

def main():    
    today = datetime.date.today()
    tournament_date = today + datetime.timedelta(days=DAYS_BEFORE_TOURNAMENT)

    current_tournaments: List[ShortTournament] = get_tournaments()

    tournaments_with_nennschluss_today = filter(lambda t: t.start.date() == tournament_date, current_tournaments)
    
    for tournament in tournaments_with_nennschluss_today:
        logger.debug(f"Creating Nennschluss Mail for {tournament.id}")
        mail = NennschlussMail(tournament= tournament)
        send_email(mail)


if __name__ == "__main__":
    main()