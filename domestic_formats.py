"""Versioned new-career regular/split schedules. No rewriting of legacy seasons."""
from functools import lru_cache
from pathlib import Path
import copy,json

@lru_cache(maxsize=1)
def catalogue():
    return json.loads((Path(__file__).resolve().parent/'assets/data/domestic_formats.json').read_text())['countries']

def specification(league):
    return catalogue().get(league.country,{}).get(str(league.tier)) if league.format_key else None

def initialize_world(career):
    if career.domestic_format_version!=1:return
    from career import CareerClub,ensure_club_uid,fictional_club_names
    for country,tiers in catalogue().items():
        archive=career.leagues[country+'|3'];names={c.name for l in career.leagues.values() if l.country==country for c in l.clubs}
        for tier,spec in tiers.items():
            league=career.leagues[country+'|'+tier];n=spec['teams'];ordered=sorted(league.clubs,key=lambda c:c.uid)
            if len(ordered)>n:
                archived=ordered[n:];league.clubs=[c for c in league.clubs if c not in archived];archive.clubs+=archived
                for c in archived:c.tier,c.league=3,archive.name
            elif len(ordered)<n:
                extra=[name for name in fictional_club_names(country,10+int(tier),96) if name not in names][:n-len(ordered)]
                if len(extra)!=n-len(ordered):raise ValueError('Insufficient expansion identities')
                for name in extra:
                    club=CareerClub(name,country,league.name,int(tier),sum(c.rating for c in ordered)/len(ordered));ensure_club_uid(club);league.clubs.append(club);names.add(name)
            league.format_key=spec['definition_id'];league.format_groups=None


def phase_rounds(phase):
    legs=phase['legs'];legs=legs if isinstance(legs,list) else [legs]*len(phase['group_sizes'])
    return max((n-1)*count for n,count in zip(phase['group_sizes'],legs))

def total_rounds(league):return sum(phase_rounds(p) for p in specification(league)['phases'])

def raw_table(clubs):return sorted(clubs,key=lambda c:(c.points,c.goal_difference,c.goals_for,c.rating),reverse=True)

def prepare_split(league):
    spec=specification(league)
    if not spec or len(spec['phases'])==1 or league.round_index<phase_rounds(spec['phases'][0]) or league.format_groups is not None:return
    phase=spec['phases'][1];ranked=raw_table(league.clubs);groups=[];offset=0
    for n in phase['group_sizes']:
        group=ranked[offset:offset+n];groups.append([c.uid for c in group]);offset+=n
    if phase['kind']=='round_robin' and phase['legs']==1:
        # Finland's final round: the upper half host five, lower half four.
        ids=groups[0];clubs={c.uid:c for c in ranked};counts={uid:0 for uid in ids}
        for r in range(len(ids)-1):
            for home,away in round_robin([clubs[uid] for uid in ids],r,1):counts[home.uid]+=1
        high=[i for i,uid in enumerate(ids) if counts[uid]==len(ids)//2]
        low=[i for i,uid in enumerate(ids) if counts[uid]==len(ids)//2-1]
        reordered=[None]*len(ids)
        for positions,source in ((high,ids[:len(ids)//2]),(low,ids[len(ids)//2:])):
            for index,uid in zip(positions,source):reordered[index]=uid
        if any(uid is None for uid in reordered):raise ValueError('Unbalanced final-round venues')
        groups=[reordered]
    # Store selection and scale once; reload must never halve points again.
    for club in league.clubs:
        rule=phase['points']
        if rule=='reset':club.points=0
        elif rule=='half_floor':club.points//=2
        elif rule=='half_ceil':club.points=(club.points+1)//2
    league.format_groups=groups

def table(league):
    prepare_split(league)
    if not league.format_groups:return raw_table(league.clubs)
    clubs={c.uid:c for c in league.clubs}
    if {uid for group in league.format_groups for uid in group}!=set(clubs):return raw_table(league.clubs)
    return [c for group in league.format_groups for c in raw_table([clubs[uid] for uid in group])]

def round_robin(clubs,round_number,legs):
    n=len(clubs);leg,rotation=divmod(round_number,n-1)
    if leg>=legs:return []
    # Match the existing balanced two-leg schedule, alternating venues per pair
    # for third/fourth legs rather than reversing every leg after the first.
    if leg%2:rotation=(n-4-rotation)%(n-1)
    rest=list(range(1,n));rest=rest[-rotation:]+rest[:-rotation] if rotation else rest;order=[0]+rest;pairs=[]
    for i in range(n//2):
        a,b=order[i],order[n-1-i]
        if (rotation%2 if i==0 else i%2):a,b=b,a
        if leg%2:a,b=b,a
        pairs.append((clubs[a],clubs[b]))
    return pairs

def pairings(league,requested):
    spec=specification(league);first=spec['phases'][0];boundary=phase_rounds(first)
    if requested<0 or requested>=total_rounds(league):return []
    if requested<boundary:return round_robin(league.clubs,requested,first['legs'])
    # Calendar previews cannot draw groups from an unfinished table.
    if league.round_index<boundary:return []
    prepare_split(league);phase=spec['phases'][1];clubs={c.uid:c for c in league.clubs};legs=phase['legs'];legs=legs if isinstance(legs,list) else [legs]*len(league.format_groups)
    return [pair for ids,count in zip(league.format_groups,legs) for pair in round_robin([clubs[uid] for uid in ids],requested-boundary,count)]

def player_finished(league,uid):
    spec=specification(league)
    if not spec or len(spec['phases'])==1:return False
    boundary=phase_rounds(spec['phases'][0])
    if league.round_index<boundary:return False
    prepare_split(league);phase=spec['phases'][1];legs=phase['legs'];legs=legs if isinstance(legs,list) else [legs]*len(league.format_groups)
    return any(uid in ids and league.round_index>=boundary+(len(ids)-1)*count for ids,count in zip(league.format_groups,legs))

def state(league):return {'key':league.format_key,'groups':copy.deepcopy(league.format_groups)} if league.format_key else None

def restore(league,data):
    if not league.format_key:
        if data is not None:raise ValueError('Unexpected domestic schedule')
        return
    if not isinstance(data,dict) or set(data)!={'key','groups'} or data['key']!=league.format_key:raise ValueError('Missing domestic schedule')
    groups=data['groups'];spec=specification(league)
    if groups is not None:
        if len(spec['phases'])!=2 or league.round_index<phase_rounds(spec['phases'][0]) or not isinstance(groups,list) or [len(g) for g in groups]!=spec['phases'][1]['group_sizes']:raise ValueError('Invalid split groups')
        flat=[uid for group in groups for uid in group]
        if len(set(flat))!=len(flat) or set(flat)!={c.uid for c in league.clubs}:raise ValueError('Invalid split identities')
    elif len(spec['phases'])==2 and league.round_index>phase_rounds(spec['phases'][0]):raise ValueError('Missing played split groups')
    league.format_groups=copy.deepcopy(groups)
