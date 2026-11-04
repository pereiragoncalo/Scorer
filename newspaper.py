"""Offline match reporting from recorded results, never invented match events."""
import copy

PHOTOS=tuple(f'assets/newspaper/match_{i}.png' for i in range(1,6))


def fresh_state():
    return dict(version=1,editions=0,negative_run=0,report=None)


def integer(value,maximum=1_000_000_000):
    return type(value) is int and 0<=value<=maximum


def clean_state(raw):
    state=fresh_state()
    if not isinstance(raw,dict) or raw.get('version')!=1:return state
    if not integer(raw.get('editions')) or not integer(raw.get('negative_run')):return state
    state.update(editions=raw['editions'],negative_run=raw['negative_run'])
    r=raw.get('report')
    if r is None:return state
    if not isinstance(r,dict):return state
    fields=('date','competition','country','home','away','home_uid','away_uid','actor_uid','status')
    if not all(isinstance(r.get(k),str) and len(r[k])<=256 and (not r[k] or r[k].isprintable()) for k in fields):return state
    score=r.get('score')
    if not isinstance(score,list) or len(score)!=2 or not all(integer(n,1000) for n in score):return state
    if not all(integer(r.get(k),1000) for k in ('goals','misses')):return state
    if not integer(r.get('photo'),4) or not integer(r.get('negative_run')):return state
    if type(r.get('standout')) is not bool:return state
    state['report']={k:copy.deepcopy(r[k]) for k in (*fields,'score','goals','misses','photo','negative_run','standout')}
    state['report']['events']=clean_events(r.get('events'),r['score'])
    return state


def clean_events(events,score):
    if not isinstance(events,list) or len(events)>64:return []
    result=[]
    for event in events:
        if not isinstance(event,dict) or not integer(event.get('minute'),110) or event.get('half') not in (1,2) or event.get('side') not in ('home','away'):return []
        result.append({k:event[k] for k in ('minute','half','side')})
    if [sum(e['side']==side for e in result) for side in ('home','away')]!=list(score):return []
    return result


def make_report(state,entry,home,away,actor_uid,score,goals,misses,moments,events=None):
    from match_moments import clean_moments
    state=copy.deepcopy(state)
    state['negative_run']=state['negative_run']+1 if goals==0 and misses>0 else 0
    own=0 if home.uid==actor_uid else 1
    not_lost=score[own]>=score[1-own]
    decisive=any(e['outcome']=='goal' and e['kind'] in ('equaliser','lead') for e in clean_moments(moments))
    standout=goals>=2 or (goals==1 and ((score[own]>score[1-own] and score[own]==1) or (decisive and not_lost)))
    report={k:str(entry.get(k,'')) for k in ('date','competition','country','status')}
    if not report['status'][:1].isdigit():report['status']=f'{score[0]}-{score[1]}'
    report.update(home=home.name,away=away.name,home_uid=home.uid,away_uid=away.uid,actor_uid=actor_uid,
                  score=list(score),goals=goals,misses=misses,photo=state['editions']%len(PHOTOS),
                  negative_run=state['negative_run'],standout=standout,events=clean_events(events,score))
    state['report']=report;state['editions']+=1
    return state


def article(report,tr,team,player,competition):
    """Return opaque display names separately from translated templates."""
    h,a=(team(report,side) for side in ('home','away'))
    hs,aws=report['score'];draw=hs==aws
    winner,loser=(h,a) if hs>aws else (a,h)
    if draw:
        headline=tr('Deadlock as {home} and {away} finish goalless',home=h,away=a) if hs==0 else tr('Nothing separates {home} and {away}',home=h,away=a)
    elif abs(hs-aws)==1:
        headline=tr('{winner} edge past {loser}',winner=winner,loser=loser)
    else:
        headline=tr('{winner} see off {loser}',winner=winner,loser=loser)
    body=[tr('{home} and {away} finished {score} in {competition}.',home=h,away=a,score=f'{hs}-{aws}',competition=competition)]
    if not draw:
        body.append(tr('A single goal separated the teams at full time.') if abs(hs-aws)==1 else tr('The final winning margin was {margin} goals.',margin=abs(hs-aws)))
    else:
        body.append(tr('The sides finished level on the match scoreboard.'))
    events=report.get('events',[])
    ledger=goal_ledger(report,tr,team)
    if ledger:body.append(' '.join(g['text'] for g in ledger))
    summary=match_summary(report,tr,team)
    body.append(summary)
    mention=''
    club=h if report['actor_uid']==report['home_uid'] else a
    if report['standout']:
        mention=tr('{player} stood out with {goals} goals for {club}.',player=player,goals=report['goals'],club=club) if report['goals']>=2 else tr('{player} caught the eye with a crucial goal for {club}.',player=player,club=club)
    elif report['negative_run']>=3:
        mention=tr('{player} endured another difficult outing: {games} consecutive appearances without a goal despite shooting chances.',player=player,games=report['negative_run'])
    if mention:body.append(mention)
    return dict(headline=headline,paragraphs=body,photo=PHOTOS[report['photo']],mentions_player=bool(mention),goals=ledger,summary=summary,lead=body[0],mention=mention)


def current_report(career):
    if career.press_state['report'] is not None:
        return career.press_state['report']
    # Legacy history has no personal performance evidence: never invent it.
    import re
    for entry in reversed(career.fixture_history):
        if not entry.get('played'):continue
        match=re.search(r'\b(\d{1,3})-(\d{1,3})\b',str(entry.get('status','')))
        if not match:continue
        r={k:str(entry.get(k,'')) for k in ('date','competition','country','home','away','home_uid','away_uid','status')}
        r.update(actor_uid='',score=[int(n) for n in match.groups()],goals=0,misses=0,photo=0,negative_run=0,standout=False)
        return r
    return None


def brief_article(report,tr,player):
    """A concise edition for small displays, with the same personal-mention rules."""
    events=report.get('events',[])
    def clock(e):
        boundary=45 if e['half']==1 else 90
        return str(e['minute']) if e['minute']<=boundary else f"{boundary}+{e['minute']-boundary}"
    if len(events)==1:
        lead=tr('Goal: {minute}.',minute=clock(events[0]))
    elif events:
        lead=tr('First goal: {first}. Last goal: {last}.',first=clock(events[0]),last=clock(events[-1]))
    else:
        h,a=report['score'];margin=abs(h-a)
        lead=tr('The sides finished level on the match scoreboard.') if not margin else tr('A single goal separated the teams at full time.') if margin==1 else tr('The final winning margin was {margin} goals.',margin=margin)
    if report['standout']:
        lead+='\n'+(tr('{player}: {goals} goals.',player=player,goals=report['goals']) if report['goals']>=2 else tr('{player}: a crucial goal.',player=player))
    elif report['negative_run']>=3:
        lead+='\n'+tr('{player}: {games} games without a goal.',player=player,games=report['negative_run'])
    return lead


def clock(event):
    boundary=45 if event['half']==1 else 90
    n=event['minute']
    return str(n) if n<=boundary else f'{boundary}+{n-boundary}'


def goal_ledger(report,tr,team):
    events=clean_events(report.get('events'),report['score'])
    result=[];score=[0,0];led=[False,False]
    for event in events:
        side=0 if event['side']=='home' else 1
        score[side]+=1
        if sum(score)==1:key="{minute}' — {team} opened the scoring ({score})."
        elif score[0]==score[1]:key="{minute}' — {team} equalised ({score})."
        elif score[side]<score[1-side]:key="{minute}' — {team} pulled a goal back ({score})."
        elif score[side]-score[1-side]==1:
            key="{minute}' — {team} regained the lead ({score})." if led[side] else "{minute}' — {team} went ahead ({score})."
        else:key="{minute}' — {team} extended the lead ({score})."
        if score[side]>score[1-side]:led[side]=True
        text=tr(key,minute=clock(event),team=team(report,event['side']),score=f'{score[0]}-{score[1]}')
        result.append(dict(text=text,minute=clock(event),side=event['side'],score=list(score)))
    if not result and sum(report['score']):
        # Older fixtures lack individual times; still account for every goal
        # by team totals without fabricating scorers or minute/order evidence.
        for side,n in zip(('home','away'),report['score']):
            if n:
                text=tr('{team}: one goal; its time was not recorded.',team=team(report,side)) if n==1 else tr('{team}: {goals} goals; individual times were not recorded.',team=team(report,side),goals=n)
                result.append(dict(text=text,side=side,score=None,minute=None))
    return result


def match_summary(report,tr,team):
    import re
    h,a=report['score'];events=clean_events(report.get('events'),report['score'])
    pens=re.search(r'pen\.\s*(\d+)-(\d+)',report['status'])
    if pens:
        winner='home' if int(pens[1])>int(pens[2]) else 'away'
        return tr('{team} won the penalty shootout after the match score finished level.',team=team(report,winner))
    if h==a:
        if h==0:return tr('Neither side broke the deadlock; the match ended without a goal.')
        if events and events[-1]['half']==2 and events[-1]['minute']>=80:
            return tr('A late equaliser settled the match at {score}.',score=f'{h}-{a}')
        return tr('The exchange of goals left the teams level at full time.')
    win=0 if h>a else 1;running=[0,0];trailed=False
    for event in events:
        running[0 if event['side']=='home' else 1]+=1
        trailed=trailed or running[win]<running[1-win]
    winner=team(report,'home' if win==0 else 'away')
    if trailed:return tr('{winner} recovered from a deficit to secure the win.',winner=winner)
    if abs(h-a)==1:return tr('{winner} secured a narrow one-goal win.',winner=winner)
    return tr('{winner} closed the match with a {margin}-goal advantage.',winner=winner,margin=abs(h-a))
