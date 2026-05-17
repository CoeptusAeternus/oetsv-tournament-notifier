#!/usr/bin/env python3
"""Container startup checks and initial state setup."""

import sys

from config import NOTIFIED_PATH, API_URL
from api import get_tournaments


def seed_notified_file() -> int:
    """Store the tournaments that already exist at startup.

    Returns the number of tournament IDs written.
    """
    tournaments = get_tournaments(API_URL)
    tournament_ids = sorted({tournament.id for tournament in tournaments})

    NOTIFIED_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTIFIED_PATH.write_text("".join(f"{tournament_id}\n" for tournament_id in tournament_ids))

    print(
        f"Startup check OK. Found {len(tournament_ids)} existing tournaments; "
        f"seeded {NOTIFIED_PATH}."
    )
    return len(tournament_ids)


def main() -> int:
    try:
        seed_notified_file()
        return 0
    except Exception as exc:
        print(f"Startup check failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
