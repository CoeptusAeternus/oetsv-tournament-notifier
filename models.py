"""Data models."""

from datetime import datetime
from pydantic import BaseModel


class Tournament(BaseModel):
    """Tournament from API."""
    id: int
    name: str
    start: datetime


class Mail:
    """Base email."""
    
    def __init__(self, tournament: Tournament):
        self.tournament = tournament
    
    @staticmethod
    def format_date(dt: datetime) -> str:
        return dt.strftime("%d.%m.%Y")
    
    def get_subject(self) -> str:
        raise NotImplementedError
    
    def get_body(self) -> str:
        raise NotImplementedError
    
    def get_sender(self) -> str:
        raise NotImplementedError


class NewTournamentMail(Mail):
    """Notification for new tournament."""
    
    def get_subject(self) -> str:
        return f"Neues Turnier im ÖTSV-Kalender gefunden: {self.tournament.name}"
    
    def get_body(self) -> str:
        date = self.format_date(self.tournament.start)
        return f"""Neues Turnier entdeckt!

Name: {self.tournament.name}
Datum: {date}

Weitere Details: https://www.tanzsportverband.at/kalender/
"""
    
    def get_sender(self) -> str:
        return "Neues Turnier Mitteilung"


class NennschlussMail(Mail):
    """Notification for registration deadline."""
    
    def get_subject(self) -> str:
        return f"Nennschluss für Turnier {self.tournament.name}"
    
    def get_body(self) -> str:
        date = self.format_date(self.tournament.start)
        return f"""Nennschlusserinnerung

Der Nennschluss für das Turnier {self.tournament.name} am {date} naht.

Registrierung: https://nennungen.schwarzgold.at
"""
    
    def get_sender(self) -> str:
        return "Nennschluss Erinnerung"
