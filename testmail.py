#!/usr/bin/env python3

import logging

from api_service import get_tournaments
from mailer import send_email
from models.mail import NennschlussMail, NewTournamentMail


def main():
    
    logging.basicConfig(encoding="utf-8", level=logging.DEBUG)
    
    tournaments = get_tournaments()
    
    if len(tournaments) == 0:
        exit(-1)
        
    t = tournaments[0]
    mail = NewTournamentMail(tournament= t)
    send_email(mail)
    mail = NennschlussMail(tournament= t)
    send_email(mail)


if __name__ == "__main__":
    main()