"""Local, deterministic club meetings and binding contract terms.

Hearing/changing an offer never signs, awards assets or consumes career RNG.
"""
import copy
from datetime import date

PREMIUMS=(0,10,20,30,50)
HOMES=('', 'studio','apartment','house')
CARS=('', 'utility','sedan','sports')
REQUEST_KEYS=('years','premium','home','car','squad')


def terms(raw):
    if not isinstance(raw,dict):return None
    if type(raw.get('years'))is not int or not 1<=raw['years']<=5:return None
    if type(raw.get('salary'))is not int or not 10<=raw['salary']<=100000000:return None
    if raw.get('home','')not in HOMES or raw.get('car','')not in CARS or type(raw.get('squad',False))is not bool:return None
    return dict(years=raw['years'],salary=raw['salary'],home=raw.get('home',''),car=raw.get('car',''),squad=raw.get('squad',False))


def expiry_date(start,years):
    try:return start.replace(year=start.year+years)
    except ValueError:return start.replace(year=start.year+years,day=28)


def clean_contract(raw):
    offer=terms(raw)
    if offer is None:return None
    if not isinstance(raw.get('club_uid'),str) or not 1<=len(raw['club_uid'])<=200:return None
    start,end=raw.get('start_season'),raw.get('end_season')
    if type(start)is not int or type(end)is not int or not 2026<=start<=9990 or end!=start+offer['years']:return None
    try:
        began=date.fromisoformat(raw['start_date']);expires=date.fromisoformat(raw['end_date'])
        if expiry_date(began,offer['years'])!=expires:return None
    except (KeyError,TypeError,ValueError):return None
    return dict(offer,club_uid=raw['club_uid'],start_season=start,end_season=end,start_date=began.isoformat(),end_date=expires.isoformat())


def clean_meetings(raw):
    result={}
    if not isinstance(raw,dict):return result
    for uid,row in list(raw.items())[:12]:
        if not isinstance(uid,str) or len(uid)>200 or not isinstance(row,dict):continue
        if row.get('club_uid')!=uid or any(not isinstance(row.get(k),str) or len(row[k])>200 for k in ('club','league')):continue
        if type(row.get('season'))is not int or not 2026<=row['season']<=9990 or type(row.get('week'))is not int or not 0<=row['week']<=100:continue
        if type(row.get('round'))is not int or not 0<=row['round']<=3 or type(row.get('starting'))is not bool:continue
        if row.get('status')not in ('offer','draft','accepted','counter'):continue
        base,offer=terms(row.get('base')),terms(row.get('offer'));request=row.get('request')
        if base is None or offer is None or not isinstance(request,dict):continue
        if type(request.get('years'))is not int or not 1<=request['years']<=5 or type(request.get('premium'))is not int or request.get('premium')not in PREMIUMS:continue
        if any(type(request.get(k))is not bool for k in ('home','car','squad')):continue
        result[uid]={k:copy.deepcopy(row[k])for k in ('club_uid','club','league','season','week','round','starting','status')}
        result[uid].update(base=base,offer=offer,request={k:request[k]for k in REQUEST_KEYS})
    return result


def ensure(c):
    """Existing saves receive two remaining seasons, without changing wages."""
    record=c.life.get('contract')
    club=c.club
    if club is not None and not c.free_agent and (record is None or record['club_uid']!=club.uid):
        from career_life import quote
        record=dict(years=2,salary=max(10,c.life.get('salary',0) or quote(c,club)),home='',car='',squad=False,club_uid=club.uid,start_season=c.season,end_season=c.season+2,start_date=c.current_date.isoformat(),end_date=expiry_date(c.current_date,2).isoformat())
        c.life['contract']=record
    return record


def remaining(c):
    record=ensure(c)
    if not record or not c.club or record['club_uid']!=c.club.uid:return 0
    end=date.fromisoformat(record['end_date']);now=c.current_date
    if end<=now:return 0
    years=end.year-now.year
    return years+(expiry_date(now,years)<end)


def expired(c):
    return bool(c.club and not c.free_agent and ensure(c) and remaining(c)==0 and not c.life['retired'])


def renewal(c):return bool(c.club and not c.free_agent and remaining(c)<=1 and not c.life['retired'])


def eligible(c,club_name,key,starting=False):
    if c.life['retired'] or key not in c.leagues:return None
    club=next((t for t in c.leagues[key].clubs if t.name==club_name),None)
    if club is None:return None
    if starting:
        return club if not c.club_name and not c.free_agent and key==c.league_key and club_name in c.offers else None
    same=c.club is not None and club.uid==c.club.uid
    if same:return club if renewal(c) else None
    return club if c.transfer_window_open and c.is_league_playable(key) and (club_name,key)in c.agent_offers else None


def base_offer(c,club):
    from career_life import quote,age
    wage=quote(c,club)
    if c.club and club.uid==c.club.uid:wage=max(wage,ensure(c)['salary'])
    return dict(years=2 if age(c)>=32 or club.rating<65 else 3,salary=max(10,wage),home='',car='',squad=False)


def open_meeting(c,club_name,key,starting=False):
    club=eligible(c,club_name,key,starting)
    if club is None:return None
    previous=copy.deepcopy(c.life)
    meetings=c.life.setdefault('negotiations',{})
    row=meetings.get(club.uid)
    if row and row['season']==c.season and row['week']==c.week and row['starting']==starting:return row
    base=base_offer(c,club);years=base['years']
    row=dict(club_uid=club.uid,club=club.name,league=key,season=c.season,week=c.week,round=0,starting=starting,status='offer',base=base,offer=copy.deepcopy(base),request=dict(years=years,premium=0,home=False,car=False,squad=False))
    c.life['negotiations']={k:v for k,v in meetings.items()if v['season']==c.season and v['week']==c.week}
    c.life['negotiations'][club.uid]=row
    if c.save() is False:c.life=previous;c.message='Unable to save your career. Please try again.';return None
    return row


def current(c,uid):
    row=c.life.get('negotiations',{}).get(uid)
    if not row or row['season']!=c.season or row['week']!=c.week:return None
    club=eligible(c,row['club'],row['league'],row['starting'])
    return row if club is not None and club.uid==uid else None


def change(c,uid,key):
    row=current(c,uid)
    if row is None or row['round']>=3 or key not in REQUEST_KEYS:return False
    before=copy.deepcopy(c.life);request=row['request']
    if key=='years':request[key]=request[key]%5+1
    elif key=='premium':request[key]=PREMIUMS[(PREMIUMS.index(request[key])+1)%len(PREMIUMS)]
    else:request[key]=not request[key]
    row['status']='draft'
    if c.save() is False:c.life=before;c.message='Unable to save your career. Please try again.';return False
    return True


def package(row):
    request=row['request'];base=row['base'];salary=base['salary']
    return dict(years=request['years'],salary=int(round(salary*(1+request['premium']/100)/10)*10),home=('apartment' if salary>=20000 else 'studio')if request['home']else '',car=('sedan' if salary>=20000 else 'utility')if request['car']else '',squad=request['squad'])


def price(offer,base,club):
    from career_life import ITEMS
    costs={row[0]:row[3]for row in ITEMS}
    squad_cost=max(20000,base['salary']*6)
    return max(0,offer['salary']-base['salary'])*12*offer['years']+costs.get(offer['home'],0)+costs.get(offer['car'],0)+(squad_cost if offer['squad']else 0)


def max_years(c):
    from career_life import age
    return 2 if age(c)>=35 else 3 if age(c)>=31 else 5


def budget(c,row,club):
    # A productive player has leverage, but small clubs still cannot fund a
    # house/car/large salary package. A long commitment helps amortise costs.
    goals=max(c.goals,c.development.get('career_goals',0))
    leverage=min(.12,goals*.003)
    return int(row['base']['salary']*12*min(row['request']['years'],max_years(c))*(.18+leverage))


def advice(c,uid):
    row=current(c,uid)
    if row is None:return ''
    club=eligible(c,row['club'],row['league'],row['starting']);offer=package(row)
    if offer['years']>max_years(c):return 'The club is unlikely to offer that many years at this stage of your career.'
    if offer['squad'] and club.rating>=99:return 'The squad is already at the top level. Ask for another benefit.'
    if offer['years']==1 and row['base']['years']>=3:return 'A one-year deal is possible, but the club is less likely to fund expensive benefits.'
    ratio=price(offer,row['base'],club)/max(1,budget(c,row,club))
    if ratio<=.65:return 'This is a realistic package. I would put it to the club.'
    if ratio<=1.:return 'This is ambitious but achievable. We may need to compromise.'
    return 'The whole package is beyond this club. Reduce the salary rise or drop a benefit.'


def propose(c,uid):
    row=current(c,uid)
    if row is None or row['round']>=3:return False
    before=copy.deepcopy(c.life);club=eligible(c,row['club'],row['league'],row['starting']);wanted=package(row);limit=budget(c,row,club)
    row['round']+=1
    if wanted['years']<=max_years(c) and price(wanted,row['base'],club)<=limit and not(wanted['squad']and club.rating>=99):
        row['offer']=wanted;row['status']='accepted'
    else:
        # The club replies with a real, signable counter-offer. Nothing is
        # awarded merely because the player asked for it.
        offer=dict(row['base'],years=min(wanted['years'],max_years(c)))
        rise=min(wanted['salary']-offer['salary'],max(0,int(limit/(12*offer['years'])/10)*10))
        offer['salary']+=rise
        for key in ('squad','home','car'):
            if not wanted[key] or (key=='squad'and club.rating>=99):continue
            candidate=dict(offer);candidate[key]=wanted[key]
            if price(candidate,row['base'],club)<=limit:offer=candidate
        row['offer']=offer;row['status']='counter'
    if c.save() is False:c.life=before;c.message='Unable to save your career. Please try again.';return False
    return True


def apply(c,club,offer):
    """Called within the existing atomic club-signing transaction."""
    offer=terms(offer)
    if offer is None:raise ValueError('Invalid contract terms')
    c.life.update(contract_club=club.uid,salary=offer['salary'],contract=dict(offer,club_uid=club.uid,start_season=c.season,end_season=c.season+offer['years'],start_date=c.current_date.isoformat(),end_date=expiry_date(c.current_date,offer['years']).isoformat()),negotiations={})
    for key in ('home','car'):
        if offer[key]:c.life['owned'][offer[key]]=c.life['owned'].get(offer[key],0)+1
    if offer['squad']:club.rating=max(club.rating,min(99.,club.rating+2.))


def sign(c,uid):
    row=current(c,uid)
    if row is None or row['status']not in ('offer','accepted','counter'):return False
    if row['starting']:return c.accept_starting_offer(row['club'],copy.deepcopy(row['offer']))
    return c.accept_transfer(row['club'],row['league'],copy.deepcopy(row['offer']))
