import httpx
import logging
import os
from typing import List
from pydantic import TypeAdapter

from models.tournamet_models import ShortTournament


logger = logging.getLogger("api_service")
logger.setLevel(logging.DEBUG)

def get_tournaments() -> List[ShortTournament]:
    
    api_url = os.getenv("API_URL")
    
    list_adapter = TypeAdapter(List[ShortTournament])
    
    response = httpx.get(api_url)
    response.raise_for_status()
    
    if response.status_code != 200:
        raise ValueError(f"API returned status code {response.status_code}")
    else:
        # Temporary Fix, while API returns duplicate tournaments
        list_with_duplcates = list_adapter.validate_python(response.json())
        unique_dict = {t.id: t for t in list_with_duplcates}
        return list(unique_dict.values())
    