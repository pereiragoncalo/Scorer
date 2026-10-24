"""Offline World presentation overlay. Canonical names, UIDs and Free kits stay intact."""
from functools import lru_cache
import json
from pathlib import Path


@lru_cache(maxsize=1)
def catalogue():
    try:
        with (Path(__file__).resolve().parent/'assets/data/world_clubs.json').open(encoding='utf-8') as stream:
            data = json.load(stream)
    except (OSError, ValueError):
        return {}  # Keep an existing career usable if local presentation data is damaged.
    if not isinstance(data, dict) or data.get('version') != 1 or not isinstance(data.get('clubs'), dict):
        return {}
    return data['clubs']


def style(club):
    row = catalogue().get(club.uid)
    # An older explicit canonical rename must not be overwritten by new defaults.
    return row if isinstance(row, dict) and isinstance(row.get('name'), str) and row.get('canonical') == club.name else None


def display_name(club):
    row = style(club)
    return row['name'] if row else club.name
