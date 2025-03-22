from pydantic import BaseModel
from typing import ClassVar

from .tournamet_models import ShortTournament


class Mail(BaseModel):
    
    tournament: ShortTournament
    
    
    def format_datetime(self, dt) -> str:
        return dt.strftime("%d.%m.%Y")
    
    def format_for_sending(self, recipients):
        if type(self) is Mail:
            raise NotImplementedError("Mail is an abstract class")

        subject = self.subject.format(self.tournament.bezeichnung)
        body = self.body.format(self.tournament.bezeichnung, self.format_datetime(self.tournament.start))

        return subject, body, self.sender

class NewTournamentMail(Mail):
    
    subject: ClassVar[str] = "Neues Turnier im ÖTSV-Kalender gefunden: {}"
    body: ClassVar[str] = \
    """
    Informationen:
    Bezeichnung: {}
    Datum: {}
    Kalender: https://www.tanzsportverband.at/kalender/
    """
    sender: ClassVar[str] = "Neues Turnier Mitteilung"


class NennschlussMail(Mail):
    
    subject: ClassVar[str] = "Nennschluss für Turnier {}"
    body: ClassVar[str] = \
    """
    Der Nennschluss für das Turnier {} am {} ist vorbei.
    https://nennungen.schwarzgold.at
    """
    sender: ClassVar[str] = "Nennschluss Erinnerung"
