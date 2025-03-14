import httpx
from typing import List
from pydantic import TypeAdapter

from models.tournamet_models import ShortTournament

API_URL = "https://oetsv.seiberte.ch/list"

def get_tournaments() -> List[ShortTournament]:
    
    list_adapter = TypeAdapter(List[ShortTournament])
    
    response = httpx.get(API_URL)
    response.raise_for_status()
    
    if response.status_code != 200:
        raise ValueError(f"API returned status code {response.status_code}")
    else:
        return list_adapter.validate_python(response.json())
    