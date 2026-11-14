"""Three saved weekly attempts, with the same deliveries as a match.

Plans use a local seed: resuming the same shot keeps its opportunity and never
advances the career RNG, fixture draw, attempt count or reward accounting.
"""
import random
from opportunity_sequences import KINDS, plan_opportunities
from career import FieldPlayer
from club_kits import HomeKit

BIB_KITS=(((.78,1.,.02,1),(.12,.17,.21,1),(.92,.96,.98,1),(.95,.98,.99,1)),
          ((1.,.20,.035,1),(.12,.17,.21,1),(.92,.96,.98,1),(.95,.98,.99,1)))

BIB_KITS=tuple(HomeKit(kit,'training_bib') for kit in BIB_KITS)

def session_seed(c):
    return (c.world_seed,c.season,c.week,c.club.uid,'training-v1')

def plan(c):
    seed=session_seed(c);rng=random.Random(str(seed))
    # The coach's specialist focus gets one attempt; the other two keep variety.
    focus=c.training_focus
    penalty=0 if focus=='penalties' else rng.randrange(3) if rng.random()<.08 else -1
    clear=next((i for i in range(3) if i!=penalty),-1) if rng.random()<.25 else -1
    kinds=list(plan_opportunities(3,clear,penalty,seed))
    if focus=='heading':
        kinds[0]=rng.choice(('cross','long_cross','corner'))
        for i in (1,2):
            if kinds[i]==kinds[0]:kinds[i]=next(k for k in KINDS if k not in kinds)
    return tuple(kinds)

def prepare(g):
    c=g.career;index=min(2,max(0,c.training_shots_taken))
    g.shot_time_limit,g.current_aim_speed=c.difficulty_profile(False)
    g._start_opportunity(plan(c)[index],(session_seed(c),index))

def add_training_teams(g):
    # Eight per side in the visible exercise: hero + seven supporting bibs,
    # seven opponents + keeper. Delivery actors count as teammates. Keep the
    # wall/chasing marker/rebound blocker and fill spare places behind play.
    players=[]
    for team,xs in (('attacker',(-10.,10.,-13.,13.)),('defender',(-9.,9.,-13.,13.))):
        target=7-sum(p.team==team for p in g.buildup_actors)
        existing=[p for p in g.field_players if p.team==team]
        if g.buildup_blocker in existing:
            existing.remove(g.buildup_blocker);existing.insert(0,g.buildup_blocker)
        selected=existing[:target]
        for i in range(target-len(selected)):
            selected.append(FieldPlayer(xs[i%len(xs)],max(15.,g.shot_origin_y+3.)+i*.7,team,float(i)))
        players.extend(selected)
    g.field_players=players
