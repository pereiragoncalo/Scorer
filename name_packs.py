"""Bounded, passive display aliases. No network, executable content or core renames."""
import json
import unicodedata

MAX_BYTES = 262144
MAX_NAMES = 4096


def validate_pack(raw, leagues, max_names=MAX_NAMES):
    if isinstance(raw, str):
        if len(raw.encode('utf-8')) > MAX_BYTES:
            raise ValueError('Name pack exceeds 256 KiB.')
        try:
            raw = json.loads(raw)
        except (ValueError, RecursionError):
            raise ValueError('Choose a valid UTF-8 JSON name pack.') from None
    if not isinstance(raw, dict) or set(raw) - {'version', 'clubs', 'leagues', 'players'} or (type(raw.get('version')) is not int or raw.get('version') != 1):
        raise ValueError('Unsupported name pack schema (expected version 1).')
    clubs = {c.uid: c for league in leagues.values() for c in league.clubs}
    cleaned = {'version': 1}
    total = 0
    for section in ('clubs', 'leagues', 'players'):
        values = raw.get(section, {})
        if not isinstance(values, dict):
            raise ValueError('Name sections must be JSON objects.')
        total += len(values)
        if total > max_names:
            raise ValueError('Too many names in one pack.')
        cleaned[section] = {}
        for key, value in values.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValueError('Name keys and values must be text.')
            if section == 'clubs':
                known = key in clubs
            elif section == 'leagues':
                known = key in leagues
            else:
                club_id, separator, slot = key.rpartition(':')
                known = separator and club_id in clubs and slot.isdigit() and 0 <= int(slot) < 12
            if not known:
                raise ValueError('Unknown name identifier. Export a template from this edition first.')
            name = unicodedata.normalize('NFC', value.strip())
            if not 2 <= len(name) <= 56 or '://' in name or any(
                unicodedata.category(c).startswith('C') or c in '<>[]' for c in name
            ):
                raise ValueError('Names must contain 2-56 printable characters, without markup or URLs.')
            cleaned[section][key] = name
    if not total:
        raise ValueError('This pack contains no names.')
    return cleaned
