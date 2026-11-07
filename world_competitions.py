"""Persistent World competition simulation; no fictitious random 'winner' labels.

Phase structures are model specifications, not a claim of verified 2026 access
lists, draw pots or official calendars. Domestic regulations are a separate audit.
"""
import copy
import hashlib
import math
import random

MODEL_VERSION=2

# Initial fields only: Libertadores transfers join Sudamericana during the season.
CLUB_FIELDS={'ucl':36,'uel':36,'uecl':36,'libertadores':32,'sudamericana':32,
             'caf_cl':16,'caf_confederation':16,'concacaf':27,'ofc':8,
             'afc_elite':24,'afc_two':32,'afc_challenge':18}
LEGACY_CLUB_FIELDS={'ucl','uel','uecl','libertadores','caf_cl','concacaf','ofc','afc_elite'}



def rng_for(*parts):
    return random.Random(':'.join(map(str,parts)))


def round_robin(teams, legs=1):
    teams=list(teams)
    if len(teams)%2:teams.append(None)
    result=[]
    for r in range(len(teams)-1):
        pairs=[]
        for i in range(len(teams)//2):
            a,b=teams[i],teams[-1-i]
            if a is not None and b is not None:pairs.append((b,a) if (r+i)%2 else (a,b))
        result.append(pairs)
        teams=[teams[0],teams[-1],*teams[1:-1]]
    return result+[[ (b,a) for a,b in row] for row in result] if legs==2 else result


def balanced_league(teams, rounds):
    """Unique opponents; Euler orientation gives equal home/away for even rounds."""
    schedule=round_robin(teams)[:rounds]
    edges=[pair for row in schedule for pair in row]
    graph={team:[] for team in teams}
    for i,(a,b) in enumerate(edges):graph[a].append((b,i));graph[b].append((a,i))
    used=set();oriented={}
    for start in teams:
        stack=[start]
        while stack:
            a=stack[-1]
            while graph[a] and graph[a][-1][1] in used:graph[a].pop()
            if not graph[a]:stack.pop();continue
            b,i=graph[a].pop();used.add(i);oriented[frozenset((a,b))]=(a,b);stack.append(b)
    return [[oriented[frozenset(pair)] for pair in row] for row in schedule]


def fixture_day(cup):
    if cup.key.startswith('domestic:'):return 0
    if cup.key.startswith('nations_'):return 3
    return 2 if cup.national else 1


def simulate_score(seed, home, away, neutral=False):
    rng=rng_for(seed)
    from career import realistic_goal_means,poisson_goal
    a,b=realistic_goal_means(home['rating'],away['rating'])
    if neutral:
        ra,rb=realistic_goal_means(away['rating'],home['rating']);a,b=(a+rb)/2,(b+ra)/2
    return [poisson_goal(rng,a),poisson_goal(rng,b)]


class Tournament:
    def __init__(self, key, title, teams, seed, *, kind='groups', groups=1,
                 rounds=6, qualifiers=2, best_thirds=0, national=False,
                 knockout_legs=2, regional_last16=False, start_week=3, slots=0, weeks=None, seeded=False, group_legs=None):
        self.key,self.title,self.seed=key,title,seed
        self.teams={t['uid']:dict(t) for t in teams}
        self.kind,self.national=kind,national
        self.qualifiers,self.best_thirds=qualifiers,best_thirds
        self.knockout_legs,self.regional_last16=knockout_legs,regional_last16
        self.groups=[];self.fixtures=[];self.active=[];self.stage='League phase';self.champion=''
        self.slots=slots;self.qualified=[];self.weeks=weeks;self.start_week=start_week
        self.direct=[];self.stage_number=0;self.last_week=start_week-1
        ids=list(self.teams)
        if not seeded:rng_for(seed,key,'draw').shuffle(ids)
        if kind=='knockout':
            self._knockout(ids,first=True);return
        if kind=='concacaf':
            self.direct=ids[:5];self._knockout(ids[5:],first=True);return
        if groups<1 or len(ids)<2*groups:raise ValueError('Invalid competition groups')
        self.groups=[ids[i::groups] for i in range(groups)]
        for index,group in enumerate(self.groups):
            size=len(group)
            schedule=balanced_league(group,rounds) if kind in ('swiss','regional') else round_robin(group,group_legs or (2 if rounds==2*(size-1) else 1))
            for r,pairs in enumerate(schedule):
                for a,b in pairs:self._add(a,b,start_week+r*2,group=index)
        self.last_week=max(f['week'] for f in self.fixtures)

    def _add(self,a,b,week,*,group=None,tie=None,leg=1):
        uid=f'{self.key}:{len(self.fixtures)}'
        record={'id':uid,'home':a,'away':b,'week':week,'stage':self.stage,'group':group,
                'tie':tie,'leg':leg,'score':None,'winner':None,'penalties':None}
        self.fixtures.append(record);self.active.append(uid)
        return record

    def table(self,index=0):
        rows={uid:{'uid':uid,'p':0,'w':0,'d':0,'l':0,'gf':0,'ga':0,'pts':0} for uid in self.groups[index]}
        for f in self.fixtures:
            if f['group']!=index or f['score'] is None:continue
            a,b=f['score'];h,v=rows[f['home']],rows[f['away']]
            for row,gf,ga in ((h,a,b),(v,b,a)):
                row['p']+=1;row['gf']+=gf;row['ga']+=ga
                row['w']+=gf>ga;row['d']+=gf==ga;row['l']+=gf<ga;row['pts']+=3 if gf>ga else 1 if gf==ga else 0
        return sorted(rows.values(),key=lambda row:(-row['pts'],-(row['gf']-row['ga']),-row['gf'],row['uid']))

    def _knockout(self,ids,*,first=False):
        if len(ids)<2 or len(set(ids))!=len(ids):raise ValueError('Invalid knockout field')
        size=1<<(len(ids)-1).bit_length()
        if size!=len(ids) and not (self.kind=='concacaf' and first):
            byes=size-len(ids);self.direct=ids[:byes];ids=ids[byes:]
        if len(ids)%2:raise ValueError('Invalid knockout field')
        self.stage_number+=1
        self.stage='Preliminary round' if first else 'Knockout playoffs' if self.stage=='League phase' and self.kind=='swiss' else ('Final' if len(ids)==2 else f'Last {len(ids)}')
        legs=1 if len(ids)==2 and self.key not in ('caf_cl','caf_confederation') else self.knockout_legs
        if self.key=='afc_elite' and len(ids)<=8:legs=1
        self.active=[];start=(self.weeks[self.stage_number-1] if self.weeks and self.stage_number<=len(self.weeks) else self.last_week+2)
        pairs=list(zip(ids[:len(ids)//2],reversed(ids[len(ids)//2:])))
        if self.regional_last16 and (len(ids)==16 or self.key in ('afc_two','afc_challenge') and len(ids)>=4):
            pairs=[]
            half=len(ids)//2
            for group in (ids[:half],ids[half:]):
                middle=len(group)//2
                pairs.extend(zip(group[:middle],reversed(group[middle:])))
        for i,(a,b) in enumerate(pairs):
            tie=f'{self.stage_number}:{i}';self._add(a,b,start,tie=tie)
            if legs==2:self._add(b,a,start+1,tie=tie,leg=2)
        self.last_week=start+legs-1

    def record(self,fixture,score):
        if fixture['score'] is not None:raise ValueError('Fixture already completed')
        if len(score)!=2 or any(type(x)is not int or not 0<=x<=99 for x in score):raise ValueError('Invalid score')
        fixture['score']=list(score)

    def _winners(self):
        ties={}
        for f in self.fixtures:
            if f['id'] in self.active:ties.setdefault(f['tie'],[]).append(f)
        winners=[]
        for tie,legs in ties.items():
            first=legs[0];a,b=first['home'],first['away'];total={a:0,b:0}
            for f in legs:
                total[f['home']]+=f['score'][0];total[f['away']]+=f['score'][1]
            if total[a]==total[b]:
                rng=rng_for(self.seed,self.key,tie,'penalties')
                strength=(self.teams[a]['rating']-self.teams[b]['rating'])/100
                winner=a if rng.random()<max(.25,min(.75,.5+strength)) else b
                legs[-1]['penalties']=[5,4] if legs[-1]['home']==winner else [4,5]
            else:winner=max(total,key=total.get)
            for f in legs:f['winner']=winner
            winners.append(winner)
        return winners

    def _progress(self):
        if self.stage=='League phase':
            tables=[self.table(i) for i in range(len(self.groups))]
            if self.key=='sudamericana':
                self.stage='Awaiting Libertadores';self.active=[];return
            if self.key=='afc_challenge':
                west=[rows[0]['uid'] for rows in tables[:3]]
                runner=max((rows[1] for rows in tables[:3]),key=lambda r:(r['pts'],r['gf']-r['ga'],r['gf'],r['uid']))
                west.append(runner['uid'])
                east=[r['uid'] for rows in tables[3:] for r in rows[:2]]
                self._knockout(west+east);return
            if self.kind=='qualifying':
                ordered=[]
                for rank in range(max(map(len,tables))):
                    ranked=[t[rank] for t in tables if rank<len(t)]
                    ranked.sort(key=lambda r:(-r['pts']/max(1,r['p']),-(r['gf']-r['ga'])/max(1,r['p']),-r['gf']/max(1,r['p']),r['uid']))
                    ordered.extend(r['uid'] for r in ranked)
                self.qualified=ordered[:self.slots];self.champion=self.qualified[0];self.stage='Completed';self.active=[];return
            if self.kind=='swiss':
                rows=tables[0];self.direct=[r['uid'] for r in rows[:8]]
                self._knockout([r['uid'] for r in rows[8:24]]);return
            qualified=[r['uid'] for rows in tables for r in rows[:self.qualifiers]]
            if self.best_thirds:
                thirds=[rows[2] for rows in tables if len(rows)>2]
                thirds.sort(key=lambda r:(-r['pts'],-(r['gf']-r['ga']),-r['gf'],r['uid']))
                qualified += [r['uid'] for r in thirds[:self.best_thirds]]
            self._knockout(qualified);return
        winners=self._winners()
        if self.stage=='Final':
            self.champion=next(f['winner'] for f in self.fixtures if f['id'] in self.active and f['stage']=='Final');self.stage='Completed';self.active=[];return
        if len(winners)==2 and self.key=='world_cup':
            losers=sorted({x for f in self.fixtures if f['id'] in self.active for x in (f['home'],f['away'])}-set(winners))
            self._knockout(winners)
            bronze=self._add(losers[0],losers[1],self.last_week,tie='bronze');bronze['stage']='Third-place match';return
        if self.direct:
            winners=self.direct+winners;self.direct=[]
        if len(winners)==1:
            self.champion=winners[0];self.stage='Completed';self.active=[]
        else:self._knockout(winners)

    def advance(self,week,protected=(),selector=None,progress_callback=None,until=None):
        protected=set(protected)
        def is_protected(f):return selector(f) if selector else bool(protected.intersection((f['home'],f['away'])))
        def due(f):return f['week']<=week and (until is None or not f.get('date') or f['date']<=until)
        while not self.champion:
            active=[f for f in self.fixtures if f['id'] in self.active]
            if not active:return None  # A cross-competition draw may still be pending.
            for f in active:
                if f['score'] is None and due(f) and not is_protected(f):
                    self.record(f,simulate_score(f'{self.seed}:{f["id"]}',self.teams[f['home']],self.teams[f['away']],neutral=f.get('neutral',False)))
            pending=[f for f in active if f['score'] is None and due(f) and is_protected(f)]
            if pending:return min(pending,key=lambda f:(f['week'],f.get('date',''),f['id']))
            if any(f['score'] is None for f in active):return None
            self._progress()
            if progress_callback:progress_callback()
        return None

    def finish(self):
        self.advance(200)
        return self.champion

    def to_dict(self):return copy.deepcopy(self.__dict__)

    @classmethod
    def from_dict(cls,data):
        if isinstance(data,dict) and data.get('kind')=='promotion':
            from promotion_playoffs import PlayoffTournament
            return PlayoffTournament.from_dict(data)
        if not isinstance(data,dict) or len(data.get('teams',{}))>128 or len(data.get('fixtures',[]))>1200:
            raise ValueError('Invalid tournament save')
        required={'key','title','seed','teams','kind','national','qualifiers','best_thirds','knockout_legs','regional_last16','groups','fixtures','active','stage','champion','direct','stage_number','last_week','slots','qualified','weeks','start_week'}
        if set(data)!=required:raise ValueError('Invalid tournament fields')
        obj=object.__new__(cls);obj.__dict__=copy.deepcopy(data)
        if any(not isinstance(getattr(obj,k),str) or not 1<=len(getattr(obj,k))<=120 for k in ('key','title','stage')):raise ValueError('Invalid competition text')
        if type(obj.national)is not bool or type(obj.qualifiers)is not int or not 0<=obj.qualifiers<=64 or type(obj.slots)is not int or not 0<=obj.slots<=64:raise ValueError('Invalid qualification format')
        if not isinstance(obj.teams,dict) or not obj.teams or not isinstance(obj.active,list) or len(obj.active)>800:raise ValueError('Invalid teams')
        ids=[]
        for uid,t in obj.teams.items():
            if not isinstance(uid,str) or len(uid)>100 or not isinstance(t,dict) or t.get('uid')!=uid or not isinstance(t.get('name'),str) or not 1<=len(t['name'])<=100 or type(t.get('rating')) not in (int,float) or not math.isfinite(t['rating']) or not 0<=t['rating']<=100:raise ValueError('Invalid competition team')
        for f in obj.fixtures:
            if not isinstance(f,dict) or set(f)-{'extra_time','date','neutral'}!={'id','home','away','week','stage','group','tie','leg','score','winner','penalties'}:raise ValueError('Invalid fixture fields')
            if not isinstance(f['id'],str) or not 1<=len(f['id'])<=150 or f['group'] is not None and (type(f['group'])is not int or not 0<=f['group']<len(obj.groups)):raise ValueError('Invalid fixture group')
            ids.append(f['id'])
            if f['home'] not in obj.teams or f['away'] not in obj.teams or f['home']==f['away'] or type(f['week']) is not int or not 0<=f['week']<=200:raise ValueError('Invalid tournament fixture')
            if 'neutral' in f and type(f['neutral'])is not bool:raise ValueError('Invalid neutral venue')
            if 'date' in f:
                from datetime import date
                if not isinstance(f['date'],str) or len(f['date'])!=10:raise ValueError('Invalid fixture date')
                date.fromisoformat(f['date'])
            for field in ('score','penalties','extra_time'):
                score=f.get(field)
                if score is not None and (not isinstance(score,list) or len(score)!=2 or any(type(x)is not int or not 0<=x<=99 for x in score)):raise ValueError('Invalid saved result')
            if f['winner'] is not None and f['winner'] not in (f['home'],f['away']):raise ValueError('Invalid winner')
        if len(set(ids))!=len(ids) or not set(obj.active)<=set(ids) or len(set(obj.active))!=len(obj.active):raise ValueError('Invalid active fixtures')
        if obj.weeks is not None and (not isinstance(obj.weeks,list) or len(obj.weeks)>12 or any(type(x)is not int or not 0<=x<=200 for x in obj.weeks) or obj.weeks!=sorted(set(obj.weeks))):raise ValueError('Invalid cup weeks')
        if obj.champion and obj.champion not in obj.teams:raise ValueError('Invalid champion')
        if obj.kind not in ('swiss','groups','concacaf','regional','knockout','qualifying') or obj.knockout_legs not in (1,2):raise ValueError('Invalid competition format')
        if any(not isinstance(g,list) or not set(g)<=set(obj.teams) for g in obj.groups):raise ValueError('Invalid groups')
        flat=[x for g in obj.groups for x in g]
        if len(flat)!=len(set(flat)) or not set(obj.direct+obj.qualified)<=set(obj.teams):raise ValueError('Duplicate group teams')
        if type(obj.stage_number) is not int or not 0<=obj.stage_number<=12 or type(obj.last_week)is not int or not 0<=obj.last_week<=200:raise ValueError('Invalid round')
        return obj



class CompetitionBook:
    def __init__(self,season,seed,leagues,entrants=None,cup_winners=None,title_holders=None):
        from career import EUROPE_COUNTRIES,SOUTH_AMERICA_COUNTRIES,NORTH_AMERICA_COUNTRIES,ASIA_COUNTRIES,AFRICA_COUNTRIES,OCEANIA_COUNTRIES,WORLD_COUNTRIES
        self.season,self.seed=season,seed;self.tournaments={};self.friendlies={};self.qualification_paths=[];self.callups={}
        self.national_membership={k:copy.deepcopy(v) for k,v in (entrants or {}).items() if k.startswith('nations_')}
        self.nations={}
        strength={'Spain':92,'Argentina':92,'France':91,'England':90,'Brazil':90,'Portugal':89,'Germany':88,'Netherlands':88,'Italy':86,'Uruguay':86,'Colombia':85,'Belgium':85,'Croatia':84,'Japan':83,'Morocco':84,'Senegal':82,'Mexico':80,'United States':80,'Iran':80,'South Korea':79,'Australia':78,'New Zealand':73}
        for country in WORLD_COUNTRIES:
            self.nations['nation:'+country]={'uid':'nation:'+country,'name':country,'country':country,'rating':strength.get(country,55+int.from_bytes(hashlib.sha256(country.encode()).digest()[:2],'big')%25),'tier':1}
        def participants(countries,count,excluded=()):
            tables=[(league.table() if league.round_index else sorted(league.clubs,key=lambda c:(-c.rating,c.uid))) for league in leagues.values() if league.tier==1 and league.country in countries]
            tables.sort(key=lambda table:(-table[0].rating,table[0].country))
            chosen=[]
            for position in range(max(map(len,tables),default=0)):
                for table in tables:
                    if position<len(table) and table[position].uid not in excluded:
                        c=table[position];chosen.append({'uid':c.uid,'name':c.name,'country':c.country,'rating':c.rating,'tier':1})
                        if len(chosen)==count:return chosen
            raise ValueError('Not enough continental entrants')
        pool={c.uid:c for l in leagues.values() for c in l.clubs}
        def prioritized(teams,ids,excluded=()):
            selected=[];seen=set(excluded)
            for uid in list(ids)+[t['uid'] for t in teams]:
                if uid in seen or uid not in pool:continue
                c=pool[uid];seen.add(uid);selected.append({'uid':uid,'name':c.name,'country':c.country,'rating':c.rating,'tier':c.tier})
                if len(selected)==len(teams):break
            return selected
        used=set()
        for key,title,rounds in [('ucl','UEFA Champions League',8),('uel','UEFA Europa League',8),('uecl','UEFA Conference League',6)]:
            teams=(entrants or {}).get(key) or participants(EUROPE_COUNTRIES,36,used)
            priority=([v for k,v in (title_holders or {}).items() if k in ('ucl','uel')] if key=='ucl' else [v for country,v in sorted((cup_winners or {}).items()) if country in EUROPE_COUNTRIES] if key=='uel' else [])
            if not entrants:teams=prioritized(teams,priority,used)
            used.update(t['uid'] for t in teams)
            self.tournaments[key]=Tournament(key,title,teams,f'{seed}:{season}',kind='swiss',rounds=rounds)
        for key,title,countries,count,groups,rounds,qualifiers,legs in [
            ('libertadores','CONMEBOL Libertadores',SOUTH_AMERICA_COUNTRIES,32,8,6,2,2),
            ('sudamericana','CONMEBOL Sudamericana',SOUTH_AMERICA_COUNTRIES,32,8,6,2,2),
            ('caf_cl','CAF Champions League',AFRICA_COUNTRIES,16,4,6,2,2),
            ('caf_confederation','CAF Confederation Cup',AFRICA_COUNTRIES,16,4,6,2,2),
            ('concacaf','Concacaf Champions Cup',NORTH_AMERICA_COUNTRIES,27,1,0,0,2),
            ('ofc','OFC Champions League',OCEANIA_COUNTRIES,8,2,3,2,1)]:
            teams=(entrants or {}).get(key) or participants(countries,count,used)
            if not entrants:
                priority=[(title_holders or {}).get(k) for k in (('libertadores','sudamericana') if key=='libertadores' else ('caf_cl','caf_confederation') if key=='caf_cl' else ())]
                teams=prioritized(teams,priority,used)
            used.update(t['uid'] for t in teams)
            self.tournaments[key]=Tournament(key,title,teams,f'{seed}:{season}',kind='concacaf' if key=='concacaf' else 'groups',groups=groups,rounds=rounds,qualifiers=qualifiers,knockout_legs=legs)
        # Explicit West/Central/South region membership (country names can contain spaces).
        west={'Afghanistan','Bahrain','Bangladesh','Bhutan','India','Iran','Iraq','Jordan','Kuwait','Kyrgyzstan','Lebanon','Maldives','Nepal','Oman','Pakistan','Palestine','Qatar','Saudi Arabia','Sri Lanka','Syria','Tajikistan','Turkmenistan','United Arab Emirates','Uzbekistan','Yemen'}
        saved=(entrants or {}).get('afc_elite');a=[t for t in saved if t['country'] in west] if saved else participants(west,12);b=[t for t in saved if t['country'] not in west] if saved else participants(set(ASIA_COUNTRIES)-west,12)
        event=Tournament('afc_elite','AFC Champions League Elite',a+b,f'{seed}:{season}',kind='regional',groups=2,rounds=8,qualifiers=8,regional_last16=True)
        # Preserve region membership after the generic draw shuffle.
        event.groups=[[t['uid'] for t in a],[t['uid'] for t in b]];event.fixtures=[];event.active=[]
        for i,group in enumerate(event.groups):
            for r,pairs in enumerate(balanced_league(group,8)):
                for x,y in pairs:event._add(x,y,3+r*2,group=i)
        event.last_week=17;self.tournaments[event.key]=event
        used.update(event.teams)
        for key,title,wcount,ecount,ngroups in (
            ('afc_two','AFC Champions League Two',16,16,8),
            ('afc_challenge','AFC Challenge League',12,6,5)):
            saved=(entrants or {}).get(key)
            a=[t for t in saved if t['country'] in west] if saved else participants(west,wcount,used)
            b=[t for t in saved if t['country'] not in west] if saved else participants(set(ASIA_COUNTRIES)-west,ecount,used)
            event=Tournament(key,title,a+b,f'{seed}:{season}',groups=ngroups,rounds=6,qualifiers=2,regional_last16=True)
            # Keep West/East separate through the regional semi-finals.
            wg=4 if key=='afc_two' else 3;eg=ngroups-wg
            aw=[t['uid'] for t in a];be=[t['uid'] for t in b]
            rng_for(seed,season,key,'west').shuffle(aw);rng_for(seed,season,key,'east').shuffle(be)
            event.groups=[aw[i::wg] for i in range(wg)]+[be[i::eg] for i in range(eg)]
            event.fixtures=[];event.active=[]
            for i,group in enumerate(event.groups):
                for r,pairs in enumerate(round_robin(group,2 if key=='afc_two' else 1)):
                    for x,y in pairs:event._add(x,y,3+r*2,group=i)
            event.last_week=max(f['week'] for f in event.fixtures)
            used.update(event.teams);self.tournaments[key]=event

        # Four explicit game leagues keep every European national team active.
        european=sorted((t for t in self.nations.values() if t['country'] in EUROPE_COUNTRIES),key=lambda t:(-t['rating'],t['uid']))
        for index,letter in enumerate('ABCD'):
            key='nations_'+letter.lower();teams=(entrants or {}).get(key) or european[index*16:(index+1)*16]
            if len(teams)<4 or season%2:continue
            groups=4 if len(teams)>=8 else 2
            self.tournaments[key]=Tournament(key,'UEFA Nations League '+letter,teams,f'{seed}:{season}',groups=groups,rounds=6,qualifiers=1,national=True,start_week=2,group_legs=2,knockout_legs=1)
        national_events=[]
        if (season+1)%4==2:
            regions=[(EUROPE_COUNTRIES,16),(AFRICA_COUNTRIES,9),(ASIA_COUNTRIES,8),(NORTH_AMERICA_COUNTRIES,6),(SOUTH_AMERICA_COUNTRIES,6),(OCEANIA_COUNTRIES,1)]
            national_events.append(('world_cup','FIFA World Cup',regions,12,8,2))
        for key,title,countries,size,groups,thirds,active in [
            ('euro','European Championship',EUROPE_COUNTRIES,24,6,4,(season+1)%4==0),
            ('afcon','Africa Cup of Nations',AFRICA_COUNTRIES,24,6,4,(season+1)%2==1),
            ('asian','AFC Asian Cup',ASIA_COUNTRIES,24,6,4,(season+1)%4==3),
            ('gold','Concacaf Gold Cup',NORTH_AMERICA_COUNTRIES,16,4,0,(season+1)%2==1),
            ('copa','Copa America',SOUTH_AMERICA_COUNTRIES+NORTH_AMERICA_COUNTRIES,16,4,0,(season+1)%4==0),
            ('ofc_nations','OFC Nations Cup',OCEANIA_COUNTRIES,8,2,0,(season+1)%4==0)]:
            if active:
                regions=[(SOUTH_AMERICA_COUNTRIES,10),(NORTH_AMERICA_COUNTRIES,6)] if key=='copa' else [(countries,size)]
                national_events.append((key,title,regions,groups,thirds,0))
        for key,title,regions,groups,thirds,wildcards in national_events:
            path={'key':key,'title':title,'groups':groups,'thirds':thirds,'wildcards':wildcards,'qualifiers':[],'created':False}
            for index,(countries,slots) in enumerate(regions):
                pool=[t for t in self.nations.values() if t['country'] in countries and t['country']!='Northern Mariana Islands']
                qkey=key+'_q'+str(index)
                self.tournaments[qkey]=Tournament(qkey,title+' qualifying',pool,f'{seed}:{season}',kind='qualifying',groups=min(slots,max(1,math.ceil(len(pool)/4))),rounds=0,national=True,slots=slots,start_week=1)
                path['qualifiers'].append(qkey)
            self.qualification_paths.append(path)
        from international_calendar import schedule_book
        schedule_book(self)

    def add_missing_continental(self,leagues,week):
        missing=set(CLUB_FIELDS)-set(self.tournaments)
        if not missing:return False
        # Preserve all existing draws/results. No retrospective personal credit.
        entrants={k:list(c.teams.values()) for k,c in self.tournaments.items() if k in CLUB_FIELDS}
        entrants.update(copy.deepcopy(self.national_membership))
        fresh=CompetitionBook(self.season,self.seed,leagues,entrants)
        for key in sorted(missing):
            cup=fresh.tournaments[key];cup.advance(max(0,week-1))
            self.tournaments[key]=cup
        self._continental_transfers()
        for key in sorted(missing):self.tournaments[key].advance(max(0,week-1))
        return True

    def _continental_transfers(self):
        cup=self.tournaments.get('sudamericana');source=self.tournaments.get('libertadores')
        if not cup or not source or cup.stage!='Awaiting Libertadores':return False
        if any(f['group'] is not None and f['score'] is None for f in source.fixtures):return False
        tables=[cup.table(i) for i in range(8)]
        cup.direct=[rows[0]['uid'] for rows in tables]
        runners=[rows[1]['uid'] for rows in tables]
        incoming=[source.teams[source.table(i)[2]['uid']] for i in range(8)]
        cup.teams.update({t['uid']:dict(t) for t in incoming})
        cup.last_week=max(cup.last_week,max(f['week'] for f in source.fixtures if f['group'] is not None))
        cup._knockout(runners+[t['uid'] for t in incoming])
        cup.stage='Knockout playoffs'
        for f in cup.fixtures:
            if f['id'] in cup.active:f['stage']=cup.stage
        return True

    def _create_finals(self):
        changed=False
        for path in self.qualification_paths:
            if path['created'] or any(not self.tournaments[k].champion for k in path['qualifiers']):continue
            selected=[];rest=[];last=0
            for key in path['qualifiers']:
                cup=self.tournaments[key];last=max(last,cup.last_week);selected.extend(cup.teams[x] for x in cup.qualified)
                rest.extend((row,cup.teams[row['uid']]) for i in range(len(cup.groups)) for row in cup.table(i) if row['uid'] not in cup.qualified)
            rest.sort(key=lambda pair:(-pair[0]['pts']/max(1,pair[0]['p']),-(pair[0]['gf']-pair[0]['ga'])/max(1,pair[0]['p']),-pair[0]['gf']/max(1,pair[0]['p']),pair[0]['uid']))
            selected.extend(t for row,t in rest[:path['wildcards']])
            self.tournaments[path['key']]=Tournament(path['key'],path['title'],selected,f'{self.seed}:{self.season}',groups=path['groups'],rounds=3,qualifiers=2,best_thirds=path['thirds'],national=True,knockout_legs=1,start_week=last+3)
            path['created']=True;changed=True
        if changed:
            from international_calendar import schedule_book
            schedule_book(self)
        return changed

    def add_domestic(self,country,leagues,weeks,*,legacy_round=0,exclude=''):
        key='domestic:'+country
        if key in self.tournaments:return self.tournaments[key]
        from domestic_rules import division_depth
        from career import EUROPE_PYRAMID_DEPTH,national_cup_name
        teams=[{'uid':c.uid,'name':c.name,'country':c.country,'rating':c.rating,'tier':c.tier} for l in leagues.values() if l.country==country and l.tier<=division_depth(country,EUROPE_PYRAMID_DEPTH) for c in l.clubs if c.uid!=exclude]
        if legacy_round:
            teams.sort(key=lambda t:(-t['rating'],t['uid']))
            # Only the remaining legacy field is redrawn; existing match history stays intact.
            actor=getattr(self,'legacy_actor','')
            chosen=teams[:max(2,min(len(teams),2**max(1,len(weeks)-legacy_round)))]
            if actor and actor not in {t['uid'] for t in chosen}:
                hero=next((t for t in teams if t['uid']==actor),None)
                if hero:chosen[-1]=hero
            teams=chosen
        cup=Tournament(key,national_cup_name(country),teams,f'{self.seed}:{self.season}',kind='knockout',knockout_legs=1,weeks=list(weeks[legacy_round:]),start_week=weeks[min(legacy_round,len(weeks)-1)])
        self.tournaments[key]=cup;return cup

    def entrants_for_next_season(self,leagues):
        cups={cup.teams[cup.champion]['country']:cup.champion for k,cup in self.tournaments.items() if k.startswith('domestic:') and cup.champion}
        holders={k:c.champion for k,c in self.tournaments.items() if not c.national and not k.startswith(('domestic:','playoff:')) and c.champion}
        fresh=CompetitionBook(self.season+1,self.seed,leagues,cup_winners=cups,title_holders=holders)
        result={k:list(c.teams.values()) for k,c in fresh.tournaments.items() if not c.national and not k.startswith('domestic:')}
        cups=[self.tournaments[k] for k in ('nations_a','nations_b','nations_c','nations_d') if k in self.tournaments]
        fields={c.key:list(c.teams.values()) for c in cups};out={c.key:set() for c in cups};incoming={c.key:[] for c in cups}
        for upper,lower in zip(cups,cups[1:]):
            up=[lower.teams[lower.table(i)[0]['uid']] for i in range(len(lower.groups))]
            bottoms=[upper.table(i)[-1] for i in range(len(upper.groups))]
            bottoms.sort(key=lambda r:(r['pts']/max(1,r['p']),(r['gf']-r['ga'])/max(1,r['p']),r['uid']))
            down=[upper.teams[r['uid']] for r in bottoms[:len(up)]]
            out[upper.key].update(t['uid'] for t in down);incoming[lower.key].extend(down)
            out[lower.key].update(t['uid'] for t in up);incoming[upper.key].extend(up)
        if not cups:result.update(copy.deepcopy(self.national_membership))
        result.update({c.key:[t for t in fields[c.key] if t['uid'] not in out[c.key]]+incoming[c.key] for c in cups})
        return result

    def complete(self):
        from international_calendar import schedule_book
        while True:
            for cup in list(self.tournaments.values()):cup.advance(200,progress_callback=lambda:schedule_book(self))
            if not (self._continental_transfers() | self._create_finals()):break


    def next_fixture(self,week,club_uid,nationality,eligible):
        from international_calendar import match_date,selected,prepare_friendlies,schedule_book
        from datetime import date,timedelta
        until=(date(self.season,7,12)+timedelta(weeks=week,days=4)).isoformat()
        pending=[];actor='nation:'+nationality
        prepare_friendlies(self,nationality)
        for cup in list(self.tournaments.values()):
            if cup.national:
                def selector(f,cup=cup):
                    return actor in (f['home'],f['away']) and selected(self,nationality,match_date(self.season,cup,f),eligible,week)
                fixture=cup.advance(week,selector=selector,progress_callback=lambda:schedule_book(self),until=until)
            else:fixture=cup.advance(week,[club_uid])
            if fixture:pending.append((match_date(self.season,cup,fixture).isoformat(),cup.key,fixture))
        if self._continental_transfers() | self._create_finals():return self.next_fixture(week,club_uid,nationality,eligible)
        if pending:
            _,key,f=min(pending,key=lambda item:(item[0],item[1],item[2]['id']))
            cup=self.tournaments.get(key);teams=cup.teams if cup else self.nations
            return key,f,teams[f['home']],teams[f['away']],cup.national if cup else True
        return None

    def record(self,key,fixture_id,score):
        if key=='friendly':
            f=self.friendlies[fixture_id]
            if f['score'] is not None:raise ValueError('Friendly already completed')
            if len(score)!=2 or any(type(x)is not int or not 0<=x<=99 for x in score):raise ValueError('Invalid score')
            f['score']=list(score);return f
        cup=self.tournaments[key];f=next(f for f in cup.fixtures if f['id']==fixture_id)
        from international_calendar import schedule_book
        cup.record(f,score);cup.advance(f['week'],(f['home'],f['away']),progress_callback=lambda:schedule_book(self))
        self._continental_transfers()
        schedule_book(self)
        return f

    def to_dict(self):
        return {'version':MODEL_VERSION,'season':self.season,'seed':self.seed,'nations':copy.deepcopy(self.nations),
                'friendlies':copy.deepcopy(self.friendlies),**({'callups':copy.deepcopy(self.callups)} if self.callups else {}),**({'national_membership':copy.deepcopy(self.national_membership)} if self.national_membership else {}),'qualification_paths':copy.deepcopy(self.qualification_paths),'tournaments':{k:v.to_dict() for k,v in self.tournaments.items()}}

    @classmethod
    def from_dict(cls,data):
        if not isinstance(data,dict) or data.get('version')!=MODEL_VERSION or len(data.get('tournaments',{}))>512 or len(data.get('friendlies',{}))>64:raise ValueError('Invalid competition book')
        obj=object.__new__(cls);obj.national_membership=copy.deepcopy(data.get('national_membership',{}));obj.callups=copy.deepcopy(data.get('callups',{}));obj.season=int(data['season']);obj.seed=int(data['seed']);obj.nations=copy.deepcopy(data['nations']);obj.friendlies=copy.deepcopy(data['friendlies']);obj.qualification_paths=copy.deepcopy(data['qualification_paths'])
        if not isinstance(obj.callups,dict) or len(obj.callups)>32 or any(not isinstance(k,str) or len(k)>150 or type(v)is not bool for k,v in obj.callups.items()):raise ValueError('Invalid call-up decisions')
        if not isinstance(obj.nations,dict) or len(obj.nations)>220:raise ValueError('Invalid nations')
        for uid,t in obj.nations.items():
            if not isinstance(t,dict) or uid!='nation:'+str(t.get('country','')) or t.get('uid')!=uid or not isinstance(t.get('name'),str) or not 1<=len(t['name'])<=100 or type(t.get('rating'))not in (int,float) or not math.isfinite(t['rating']) or not 0<=t['rating']<=100:raise ValueError('Invalid nation')
        if not isinstance(obj.national_membership,dict) or len(obj.national_membership)>4 or any(k not in ('nations_a','nations_b','nations_c','nations_d') or not isinstance(v,list) or len(v)>16 or any(not isinstance(t,dict) or t.get('uid') not in obj.nations or t!=obj.nations[t['uid']] for t in v) for k,v in obj.national_membership.items()):raise ValueError('Invalid Nations League membership')
        obj.tournaments={k:Tournament.from_dict(v) for k,v in data['tournaments'].items()}
        from datetime import date
        for f in [f for cup in obj.tournaments.values() for f in cup.fixtures]+list(obj.friendlies.values()):
            if f.get('date') and (date.fromisoformat(f['date'])-date(obj.season,7,12)).days//7!=f['week']:raise ValueError('Fixture date and season week disagree')
        if len(obj.qualification_paths)>8 or any(not isinstance(p,dict) or not set(p.get('qualifiers',[]))<=set(obj.tournaments) for p in obj.qualification_paths):raise ValueError('Invalid qualification path')
        for k,cup in obj.tournaments.items():
            if k!=cup.key:raise ValueError('Competition key mismatch')
        for f in obj.friendlies.values():
            if f.get('home') not in obj.nations or f.get('away') not in obj.nations or f['home']==f['away'] or type(f.get('week'))is not int or not 0<=f['week']<=200:raise ValueError('Invalid friendly')
            if f.get('score') is not None and (not isinstance(f['score'],list) or len(f['score'])!=2 or any(type(x)is not int or not 0<=x<=99 for x in f['score'])):raise ValueError('Invalid friendly result')
        from international_calendar import prepare_friendlies
        prepare_friendlies(obj)
        return obj
