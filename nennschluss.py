#!/usr/bin/env python3
"""Notify about registration deadlines (Nennschluss)."""

import sys
from datetime import datetime, timedelta
from config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, RECIPIENTS, API_URL, DAYS_BEFORE_TOURNAMENT
from api import get_tournaments
from mail import send_email
from models import NennschlussMail


def main():
    try:
        # Get current tournaments from API
        tournaments = get_tournaments(API_URL)
        
        # Calculate nennschluss date
        today = datetime.now().date()
        nennschluss_date = today + timedelta(days=DAYS_BEFORE_TOURNAMENT)
        
        # Find tournaments with nennschluss today
        for tournament in tournaments:
            if tournament.start.date() == nennschluss_date:
                mail = NennschlussMail(tournament)
                send_email(mail, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, RECIPIENTS)
                print(f"Nennschluss notification sent for {tournament.id}: {tournament.name}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
