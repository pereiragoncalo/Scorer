"""Two-division access models; actual match results decide every playoff place."""
from functools import lru_cache
from pathlib import Path
import json
from promotion_playoffs import PlayoffTournament

@lru_cache(maxsize=1)
def catalogue():
    return json.loads((Path(__file__).resolve().parent/'assets/data/domestic_profiles.json').read_text())

def profile(country,runtime=False):
    result=dict(catalogue()['profiles'].get(country,dict(direct=3,shape='',places=[],upper=[],reserve_direct=3,reserve_shape='',reserve_places=[])))
    if runtime:
        updates={
            'Sweden':dict(direct=2,shape='swedish',places=[3,4],upper=[-3]),
            'South Africa':dict(direct=1,shape='group_cross',places=[2,3],upper=[-2],reserve_direct=2,reserve_shape='',reserve_places=[]),
            'China':dict(direct=2,shape='',places=[],upper=[],reserve_direct=2,reserve_shape='',reserve_places=[]),
            'Vietnam':dict(direct=2,shape='',places=[],upper=[],reserve_direct=2,reserve_shape='',reserve_places=[]),
        }
        result.update(updates.get(country,{}))
    return result

def eligible_table(league):
    blocked=set(catalogue()['ineligible_for_first_division'])
    return [c for c in league.table() if c.uid not in blocked]

def team(c):return dict(uid=c.uid,name=c.name,country=c.country,tier=c.tier,rating=c.rating,points=c.points)

def game(key,a,b,legs=2,decision='extra_pens',title=None,qualifies=False,neutral=False,seed_second=False):
    if title is None:
        title='Preliminary round' if key.startswith('pre') else 'Semi-finals' if key.startswith('semi') else 'Final' if key.startswith(('final','cross','first')) else 'Promotion/relegation playoff'
    return dict(id=key,home=a,away=b,legs=legs,decision=decision,title=title,qualifies=qualifies,neutral=neutral,seed_second=seed_second)

def build_tournament(country,upper,lower,seed,week,*,reserve=False,queue=None):
    p=profile(country,bool(lower.format_key));shape=p['reserve_shape'] if reserve else p['shape'];plan=[]
    if not shape:return None
    top=lower.table() if reserve else eligible_table(lower);high=upper.table() if not reserve else top
    if reserve:
        top=[queue[i] for i in range(len(queue))]
        positions=range(p['reserve_direct']+1,p['reserve_direct']+1+len(p['reserve_places']))
        selected=[top[i-1] for i in positions]
        challengers=[lower.table()[i] for i in p['reserve_places']]
    else:
        selected=[top[i-1] for i in p['places'] if i<=len(top)]
        challengers=[high[i] for i in p['upper']]
    by_uid={c.uid:c for c in selected+challengers}
    ranks={c.uid:i for i,c in enumerate(top)}
    def uid(i):return selected[i].uid
    def cross(a,b,key='final'):
        if country=='Germany':a,b=b,a
        elif country=='Portugal':
            from world_competitions import rng_for
            if rng_for(seed,country,key,'venue').randrange(2):a,b=b,a
        return game(key,a,b)
    if shape=='group_cross':
        from world_competitions import Tournament
        cup=Tournament('playoff:'+country+':2',country+' Promotion playoff',[team(c) for c in selected+challengers],str(seed),kind='qualifying',groups=1,group_legs=2,slots=1,start_week=week)
        for fixture in cup.fixtures:fixture['week']=week+(fixture['week']-week)//2
        cup.last_week=max(f['week'] for f in cup.fixtures)
        return cup
    if shape=='swedish':
        plan=[[game('preliminary',uid(1),uid(0))],[cross('win:preliminary',challengers[0].uid)]]
    elif shape in ('cross','parallel_cross'):
        if len(selected)!=len(challengers):raise ValueError('Invalid cross-division field')
        plan=[[cross(a.uid,b.uid,'final'+str(i)) for i,(a,b) in enumerate(zip(selected,reversed(challengers)))]]
    elif shape=='playout':
        a,b=lower.table()[-5:-3];by_uid={a.uid:a,b.uid:b};ranks={a.uid:0,b.uid:1}
        if a.points-b.points>4:return None
        plan=[[game('survival',b.uid,a.uid,decision='extra_pens' if a.points==b.points else 'rank',title='Relegation playout')]]
    elif shape=='french':
        plan=[[game('preliminary',uid(1),uid(2),1)],[game('semifinal',uid(0),'win:preliminary',1)],[cross('win:semifinal',challengers[0].uid)]]
    elif shape=='scottish':
        plan=[[game('preliminary',uid(2),uid(1))],[game('semifinal','win:preliminary',uid(0))],[cross('win:semifinal',challengers[0].uid)]]
    elif shape=='norwegian':
        plan=[[game('p1',uid(2),uid(3),1)],[game('p2',uid(1),'win:p1',1)],[game('p3',uid(0),'win:p2',1)],[cross('win:p3',challengers[0].uid)]]
    elif shape=='parallel':
        plan=[[game('final1',uid(3),uid(0),decision='rank'),game('final2',uid(2),uid(1),decision='rank')]]
    elif shape in ('four_two','four_single','four_two_cross'):
        legs=1 if shape=='four_single' else 2;policy='rank' if country=='Japan' else 'extra_rank' if country=='Spain' else 'extra_pens'
        plan=[[game('semi1',uid(3),uid(0),legs,policy),game('semi2',uid(2),uid(1),legs,policy)],[game('final','win:semi2','win:semi1',legs,policy,seed_second=legs==2)]]
        if challengers:plan.append([cross('win:final',challengers[0].uid,'cross')])
    elif shape in ('six','italian'):
        if shape=='italian':
            if top[2].points-top[3].points>14:return None
            selected=[club for club in selected if top[2].points-club.points<=14]
            by_uid={club.uid:club for club in selected}
        n=len(selected);prelim='extra_rank' if shape=='italian' else 'extra_pens';semi='rank' if shape=='italian' else 'extra_pens'
        final_legs=2 if shape=='italian' else 1;final_policy='rank' if shape=='italian' else 'extra_pens'
        if n>4:
            byes=8-n;rest=[uid(i) for i in range(byes,n)];opening=[];winners=[]
            for i in range(len(rest)//2):
                key='pre'+str(i);opening.append(game(key,rest[i],rest[-1-i],1,prelim));winners.append('win:'+key)
            plan.append(opening);refs=[uid(i) for i in range(byes)]+winners
        else:refs=[uid(i) for i in range(n)]
        if len(refs)>2:
            bye=1 if len(refs)==3 else 0;playing=refs[bye:];semis=[];next_refs=refs[:bye]
            for i in range(len(playing)//2):
                key='semi'+str(i);semis.append(game(key,playing[-1-i],playing[i],2,semi));next_refs.append('win:'+key)
            plan.append(semis);refs=next_refs
        plan.append([game('final',refs[1],refs[0],final_legs,final_policy,neutral=shape=='six',seed_second=final_legs==2)])
    elif shape=='turkish':
        plan=[[game('pre1',uid(1),uid(4),1),game('pre2',uid(2),uid(3),1)],
              [game('semi','win:pre2','win:pre1')],[game('final',uid(0),'win:semi',1,neutral=True)]]
    elif shape=='argentine':
        # Two game groups ranked from the combined table; neutral first promotion
        # final, its loser joins the reducido after the opening round.
        selected=top[:min(16,len(top)-p['reserve_direct'])];by_uid={c.uid:c for c in selected};a,b=selected[:2];rest=selected[2:]
        opening=[game('first',a.uid,b.uid,1,qualifies=True,neutral=True)]
        refs=[]
        if len(rest)%2:refs.append(rest.pop(0).uid)
        for i in range(len(rest)//2):
            key='r1_'+str(i);opening.append(game(key,rest[-1-i].uid,rest[i].uid,1,'rank'));refs.append('win:'+key)
        refs=['lose:first']+refs;plan=[opening];round_no=2
        while len(refs)>1:
            size=1<<(len(refs)-1).bit_length();byes=size-len(refs);next_refs=refs[:byes];playing=refs[byes:];games=[]
            for i in range(len(playing)//2):
                key='r'+str(round_no)+'_'+str(i);games.append(game(key,playing[-1-i],playing[i],2,'rank'));next_refs.append('win:'+key)
            plan.append(games);refs=next_refs;round_no+=1
    else:raise ValueError('Unknown playoff shape '+shape)
    key='playoff:'+country+(':reserve' if reserve else ':2')
    return PlayoffTournament(key,country+(' Relegation playoff' if reserve else ' Promotion playoff'),[team(c) for c in by_uid.values()],str(seed),plan,start_week=week,ranks={uid:rank for uid,rank in ranks.items() if uid in by_uid})


def direct_up(lower):
    p=profile(lower.country,bool(lower.format_key));n=p['direct']
    if p['shape']=='italian':
        t=eligible_table(lower)
        if t[2].points-t[3].points>14:n=3
    return eligible_table(lower)[:n]


def movements(upper,lower,book):
    """Freeze and validate participants before moving either boundary."""
    up=direct_up(lower);p=profile(lower.country,bool(lower.format_key));cup=book.tournaments.get('playoff:'+lower.country+':2')
    if cup:
        if not cup.champion:raise ValueError('Unplayed promotion playoff')
        available={c.uid:c for c in upper.clubs+lower.clubs}
        up += [available[uid] for uid in cup.qualified if uid in {c.uid for c in lower.clubs}]
    count=len(direct_up(lower)) if p['upper'] else len(up)
    down=upper.table()[-count:] if count else []
    if cup and p['upper']:
        candidates=[upper.table()[i] for i in p['upper']]
        down += [c for c in candidates if c.uid not in cup.qualified]
    if len(up)!=len(down):raise ValueError('Unbalanced promotion results')
    return up,down


def reserve_movements(lower,queue,book):
    p=profile(lower.country,bool(lower.format_key));n=p['reserve_direct'];down=lower.table()[-n:] if n else [];up=queue[:n]
    cup=book.tournaments.get('playoff:'+lower.country+':reserve')
    if cup:
        if not cup.champion:raise ValueError('Unplayed relegation playoff')
        active={c.uid:c for c in lower.clubs};reserve={c.uid:c for c in queue}
        if p['reserve_shape']=='playout':
            losers=[c for c in lower.table()[-5:-3] if c.uid not in cup.qualified];down+=losers;up=queue[:len(down)]
        else:
            for f in cup.fixtures:
                if f['leg']!=1:continue
                winner=cup.results[f['tie']]
                if winner in reserve:
                    up.append(reserve[winner]);down.append(active[next(uid for uid in (f['home'],f['away']) if uid in active)])
    elif p['reserve_shape']=='playout':down=lower.table()[-(n+1):];up=queue[:len(down)]
    return down,up
