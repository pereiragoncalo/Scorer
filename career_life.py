"""Local contract, money and ageing. Purchases never award goals or attributes."""
import copy,math
ITEMS=(
 ('studio','home','Studio apartment',80000),('apartment','home','City apartment',200000),('house','home','Family house',550000),('mansion','home','Mansion',3500000),
 ('utility','car','Compact car',10000),('sedan','car','Executive sedan',35000),('sports','car','Sports car',140000),('supercar','car','Supercar',750000),
 ('rose','gift','A rose',25),('flowers','gift','Flower bouquet',80),('necklace','gift','Gold necklace',2500),('handbag','gift','Designer handbag',6000),
 ('casual','clothes','Casual outfit',60),('smart','clothes','Smart outfit',300),('suit','clothes','Tailored suit',1500),('designer','clothes','Designer wardrobe',12000))
def fresh(c):return dict(version=2,contract=None,negotiations={},paid_month=c.current_date.year*12+c.current_date.month,start_season=2026,balance=0,salary=0,contract_club='',paid_at=c.season*52+c.week,owned={},retired=False,retirement_seen=0,favourite='',private_meeting='',drought_talk=0,offer_talk='',injury_name='',injury_games=0,injury_fixture='')
def clean(raw,c):
 d=fresh(c)
 if not isinstance(raw,dict) or raw.get('version') not in (1,2):return d
 for key in ('start_season','balance','salary','paid_at','paid_month','retirement_seen','drought_talk'):
  v=raw.get(key)
  if type(v)is int and 0<=v<=100000000000:d[key]=v
 if raw.get('version')==1:d['salary']=round(d['salary']*52/12)
 d['start_season']=min(c.season,max(2026,d['start_season']))
 for key in ('contract_club','favourite','offer_talk','private_meeting','injury_fixture'):
  if isinstance(raw.get(key),str) and len(raw[key])<=(600 if key=='injury_fixture' else 100) and raw[key].isprintable():d[key]=raw[key]
 from injuries import NAMES
 if raw.get('injury_name') in NAMES and type(raw.get('injury_games')) is int and 0<=raw['injury_games']<=3:
  d['injury_name']=raw['injury_name'];d['injury_games']=raw['injury_games']
 from contract_negotiation import clean_contract,clean_meetings
 d['contract']=clean_contract(raw.get('contract'));d['negotiations']=clean_meetings(raw.get('negotiations'))
 d['retired']=raw.get('retired') is True
 if isinstance(raw.get('owned'),dict):d['owned']={k:v for k,v in raw['owned'].items() if k in {i[0] for i in ITEMS} and type(v)is int and 1<=v<=100000}
 return d
def age(c):return 18+max(0,c.season-c.life['start_season'])
def decline(c):return 1+max(0,age(c)-38)*.13
def quote(c,club):
 from league_status import league_status
 status=league_status(club.country,club.tier)
 return int(round((60+status**2*.9)*max(.35,(club.rating-35)/35)*(1+min(2.,c.goals/max(5,c.matches)))*52/12/10)*10)
def salary(c):
 if not c.club or c.free_agent or c.life['retired']:return 0
 record=c.life.get('contract')
 if record and record['club_uid']==c.club.uid:return record['salary'] if record['end_date']>c.current_date.isoformat() else 0
 return quote(c,c.club)
def sync(c):
 """One payment per calendar month; fixtures and reloads never duplicate it."""
 if not hasattr(c,'life'):c.life=fresh(c)
 d=c.life;uid=c.club.uid if c.club and not c.free_agent and not d['retired'] else ''
 now=c.current_date.year*12+c.current_date.month
 from contract_negotiation import ensure
 record=ensure(c)
 until=min(now,int(record['end_date'][:4])*12+int(record['end_date'][5:7])) if record and record['club_uid']==d['contract_club'] else now
 elapsed=max(0,min(24,until-d.get('paid_month',now)))
 if not d['retired']:d['balance']+=elapsed*d['salary']
 d['paid_month']=max(d.get('paid_month',now),now)
 if uid!=d['contract_club']:d['contract_club']=uid;d['salary']=salary(c)
 if record and uid==record['club_uid']:d['salary']=record['salary'] if record['end_date']>c.current_date.isoformat() else 0
def purchase(c,key):
 row=next((i for i in ITEMS if i[0]==key),None)
 if not row:return False
 _,category,_,cost=row;d=c.life
 if d['balance']<cost or (category!='gift' and key in d['owned']):return False
 before=copy.deepcopy(d);d['balance']-=cost;d['owned'][key]=d['owned'].get(key,0)+1
 if c.save() is False:c.life=before;return False
 return True
def retirement_due(c):return age(c)>=38 and not c.life['retired'] and c.life['retirement_seen']!=c.season
def retirement(c,retire):
 if age(c)<38:return False
 before=copy.deepcopy(c.life);c.life.update(retired=bool(retire),retirement_seen=c.season)
 if c.save() is False:c.life=before;return False
 return True


def best_assets(c):
 """Best owned item in each portrait category, independent of purchase order."""
 return {kind:max((row for row in ITEMS if row[1]==kind and c.life['owned'].get(row[0],0)>0),key=lambda row:row[3],default=None) for kind in ('home','car','clothes')}
