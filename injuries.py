"""Saved short injuries. Recovery is counted in missed fixtures, never menu visits."""
import hashlib,random
NAMES=('Ankle sprain','Calf strain','Thigh knock','Groin strain','Bruised knee','Hamstring strain')
def active(c):return c.life.get('injury_games',0)>0
def probability(c):return .01+.02*(1-max(0.,min(20.,c.stamina))/20.)
def complete(c,absent):
    entry=c.fixture_history[-1]
    key='|'.join(str(entry.get(k,'')) for k in ('date','competition','home','away'))
    if c.life.get('injury_fixture')==key:return
    c.life['injury_fixture']=key
    if absent:
        entry['played']=True;entry['player_played']=False;entry['absence']=c.life['injury_name']
        c.life['injury_games']=max(0,c.life['injury_games']-1)
        return
    rng=random.Random(hashlib.sha256(f"injury-v1:{c.world_seed}:{key}".encode()).digest())
    if rng.random()<probability(c):
        c.life['injury_name']=rng.choice(NAMES);c.life['injury_games']=rng.randint(1,3)
def label(c,tr):
    if not active(c):return ''
    return tr('{injury} · Out for {games} match(es)',injury=tr(c.life['injury_name']),games=c.life['injury_games'])
