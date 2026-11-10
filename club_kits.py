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

class HomeKit(tuple):
    def __new__(cls,colours,pattern='striped'):
        obj=super().__new__(cls,colours);obj.pattern=pattern;return obj

def shirt_pattern(club):
    from club_profiles import catalogue as profiles
    row=profiles().get(club.uid,{})
    if row.get('shirt_pattern') in ('plain','striped'):return row['shirt_pattern']
    plain_uids = ('09746d7dd23654a57132', '0a57fa8e31a868f0b6e9', '1b90a5a7b45d01807901', '1dd757d88c0069bcd7cd', '2128f2b8f01e8eeecf3a', '25978b18d31edad02b79', '26d175cbef2faf758d99', '28287e8e6bd50eb49e5d', '2d8ed6622c1975e49c94', '3aafb272e8752af57673', '4279d0e1c7fb3bc28cff', '582cdd1845afc7c3faff', '5d27df05665c0406256b', '5f9f7033f562b3fe6218', '70016252382c95789326', '700e13942a34696fdae5', '79f1e283c133ea287c86', '7db45bcfc5d635bf6a33', '8e8904232485cb82559c', '9e90b993b2ca6783b176', 'a236192def0f049f14cd', 'a2fb9f1e2eb7fac49500', 'b1d1ccbb9e77bc53c029', 'c8d6431e000ec7467295', 'cbd600ef2f5d278ae21d', 'd1e35165727184231fcf', 'fd1111e5e54231a2a93f', 'fda9c90903e5a56a33bd')
    return 'plain' if club.uid in plain_uids else 'striped'
