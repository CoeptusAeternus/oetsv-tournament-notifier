"""API client."""

import httpx
from typing import List
from pydantic import TypeAdapter
from models import Tournament


def get_tournaments(api_url: str) -> List[Tournament]:
    """Fetch tournaments from API."""
    response = httpx.get(api_url, timeout=30)
    response.raise_for_status()
    
    adapter = TypeAdapter(List[Tournament])
    tournaments = adapter.validate_python(response.json())
    
    # Remove duplicates if API returns them
    unique = {t.id: t for t in tournaments}
    return list(unique.values())
