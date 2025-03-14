import os
from typing import List

from api_service import get_tournaments
from mailer import send_email
from models.mail import NewTournamentMail
from models.tournamet_models import ShortTournament

STARTUP_RUN = True

NOTIFIED_FILE = ""

def create_notified_file()-> None:
    if not os.path.exists(NOTIFIED_FILE):
        with open(NOTIFIED_FILE, "w") as f:
            f.write("")

def get_notified_tournaments() -> List[int]:
    if not os.path.exists(NOTIFIED_FILE):
        create_notified_file()
    
    with open(NOTIFIED_FILE, "r") as f:
        return [int(line.strip()) for line in f.readlines()]

def add_to_notified_file(tournament: ShortTournament) -> None:
    with open(NOTIFIED_FILE, "a") as f:
        f.write(f"{tournament.id}\n")
    
def main():
    current_tournaments = get_tournaments()
    
    if STARTUP_RUN:
        create_notified_file()
        for tournament in current_tournaments:
            add_to_notified_file(tournament)
    
        STARTUP_RUN = False
    else:
        notified_tournaments = get_notified_tournaments()
        new_tournaments = filter(lambda t: t.id not in notified_tournaments, current_tournaments)
        
        for tournament in new_tournaments:
            mail = NewTournamentMail(tournament)
            add_to_notified_file(tournament)
            send_email(mail)



if __name__ == "__main__":
    main()
