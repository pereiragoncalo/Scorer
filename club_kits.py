"""Offline real home colours, bound to club UID rather than editable names."""
from functools import lru_cache
import json
from pathlib import Path
import re


@lru_cache(maxsize=1)
def catalogue():
    try:
        data = json.loads((Path(__file__).resolve().parent / 'assets/data/club_kits.json').read_text(encoding='utf-8'))
        if data.get('version') != 1 or not isinstance(data.get('clubs'), dict):
            return {}
        return {uid: tuple(row['home']) for uid, row in data['clubs'].items()
                if isinstance(row, dict) and isinstance(row.get('home'), list)
                and len(row['home']) == 4
                and all(isinstance(c, str) and re.fullmatch('[0-9A-Fa-f]{6}', c) for c in row['home'])}
    except (OSError, ValueError, AttributeError):
        return {}


def home_colours(club):
    return catalogue().get(club.uid)
