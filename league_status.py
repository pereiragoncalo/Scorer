"""Game league prestige, with explicit source provenance; not a FIFA league ranking."""
import json,hashlib
from functools import lru_cache
from pathlib import Path
@lru_cache(maxsize=1)
def data():
 try:return json.loads((Path(__file__).parent/'assets/data/league_status.json').read_text())
 except (OSError,ValueError):return {'countries':{},'clubs':{}}
def league_status(country,tier=1):
 row=data()['countries'].get(country,{})
 return max(1,round(row.get('status',35)*(.72 if tier==2 else 1)))
def club_rating(club):
 row=data()['clubs'].get(club.uid)
 if not row or not row.get('seasons'):
  # Stable country-scaled game baseline, explicitly not an invented historical table.
  origin=data().get('origin_tiers',{}).get(club.uid,club.tier)
  factor=1. if origin==1 else .72 if origin==2 else .55
  country=data()['countries'].get(club.country,{}).get('status',35)
  noise=int.from_bytes(hashlib.sha256((club.uid or club.name).encode()).digest()[:4],'big')/0xffffffff
  return round(38+country*factor*.4+(noise-.5)*12,2)
 # Real completed tables anchor the baseline; career results remain stochastic.
 return row['rating']
def standout(c):return c.matches>=8 and c.goals/max(1,c.matches)>=.5

def league_band(country,tier=1):
 value=league_status(country,tier)
 return 5 if value>=90 else 4 if value>=75 else 3 if value>=60 else 2 if value>=45 else 1
def status_label(country,tier=1):return ('Local','Developing','Established','High','Elite')[league_band(country,tier)-1]
