#!/usr/bin/env python3
"""Notify about new tournaments."""

import sys
from config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, RECIPIENTS, API_URL, NOTIFIED_PATH
from api import get_tournaments
from mail import send_email
from models import NewTournamentMail


def main():
    try:
        # Get current tournaments from API
        tournaments = get_tournaments(API_URL)
        
        # Read already notified tournaments
        notified = set()
        if NOTIFIED_PATH.exists():
            notified = {int(line.strip()) for line in NOTIFIED_PATH.read_text().splitlines()}
        
        # Find new tournaments
        new_tournaments = [t for t in tournaments if t.id not in notified]
        
        # Send emails for new tournaments
        for tournament in new_tournaments:
            mail = NewTournamentMail(tournament)
            send_email(mail, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, RECIPIENTS)
            
            # Mark as notified
            with open(NOTIFIED_PATH, "a") as f:
                f.write(f"{tournament.id}\n")
            
            print(f"Notified about tournament {tournament.id}: {tournament.name}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
