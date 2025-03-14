import os
import datetime
from typing import List

from api_service import get_tournaments
from mailer import send_email
from models.tournamet_models import ShortTournament
from models.mail import NennschlussMail

DAYS_BEFORE_TOURNAMENT = os.getenv("DAYS_BEFORE_TOURNAMENT", 14)

def main():
    today = datetime.date.today()
    tournament_date = today + datetime.timedelta(days=DAYS_BEFORE_TOURNAMENT)

    current_tournaments: List[ShortTournament] = get_tournaments()

    tournaments_with_nennschluss_today = filter(lambda t: t.start.date() == tournament_date, current_tournaments)
    
    for tournament in tournaments_with_nennschluss_today:
        mail = NennschlussMail(tournament)
        send_email(mail)


if __name__ == "__main__":
    main()