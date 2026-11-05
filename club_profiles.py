"""Offline identity-bound club information; no invented factual history."""
from functools import lru_cache
import json,math
from dataclasses import dataclass
from pathlib import Path

@lru_cache(maxsize=1)
def catalogue():
    try:
        data=json.loads((Path(__file__).resolve().parent/'assets/data/club_profiles.json').read_text(encoding='utf8'))
        return data['clubs'] if data.get('version')==1 and isinstance(data.get('clubs'),dict) else {}
    except (OSError,ValueError,KeyError):return {}

def profile(club):
    row=catalogue().get(getattr(club,'uid',''),{})
    return dict(founded=row.get('founded'),stadium=row.get('stadium'),capacity=row.get('capacity'),honours=row.get('honours',[]),supporters=row.get('supporters'),source=row.get('source'),revision=row.get('revision'))

def stadium_capacity(club):
    value=profile(club)['capacity']
    if type(value)is int and 250<=value<=150000:return value
    # Fictional/unverified venues use a bounded game model, never a factual
    # capacity in the club information card.
    rating=getattr(club,'rating',65) or 65
    return max(2500,min(40000,round((rating-40)*650/500)*500))

def career_titles(career,uid):
    return [row for row in career.honours['trophies'] if row['team_uid']==uid and not row['competition'].startswith('scorer:')]

@dataclass(frozen=True)
class Ground:
    capacity:int
    lower_rows:int
    upper_rows:int
    @property
    def tiers(self):return 2 if self.upper_rows else 1

def ground(capacity):
    capacity=max(250,min(150000,int(capacity)))
    lower=max(6,round(6+12*math.sqrt(min(capacity,40000)/40000)))
    upper=0 if capacity<=40000 else min(22,round(8+10*math.sqrt((capacity-40000)/60000)))
    return Ground(capacity,lower,upper)
