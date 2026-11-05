"""Bounded, local career goals, focused practice and recoverable coach trust.

No goal outcome is awarded by this module. Skills only adjust explicit control
parameters; trust never removes the trained/morale minimum opportunity floors.
"""
import copy

FOCI=('low','placed','heading','penalties')
NAMES=dict(zip(FOCI,('Low finishing','Placed finishing','Heading','Penalties')))
HINTS={
 'low':'Aim below 0.9 m. Each level makes low match finishes 0.6% faster.',
 'placed':'Aim for the outer thirds. Each level slows normal match aiming by 1.2%.',
 'heading':'Practise headers. Each level adds 0.1 s and steadies header aiming.',
 'penalties':'Practise from the spot. Each level adds 0.08 s and steadies penalty aiming.',
}
ROLES=('Substitute','Starter','Key player')

def integer(v,maximum=1_000_000):return type(v)is int and 0<=v<=maximum

def needed(level):return 60+20*level

def fresh(season=2026,goals=0,matches=0):
    return dict(version=1,season=season,tracked_since=season,club='',trust=50,peak_trust=50,
        last_change=0,last_minutes=0,last_role='Starter',focus='placed',
        skills={k:{'level':0,'xp':0} for k in FOCI},sessions=0,session=None,
        season_goals=goals,season_matches=matches,goal_target=10,season_earned=[],
        career_goals=goals,career_matches=matches,transfers=0,minutes=0,archive=[])

def clean(raw,season,goals=0,matches=0):
    fallback=fresh(season,max(0,goals),max(0,matches))
    if not isinstance(raw,dict) or type(raw.get('version'))is not int or raw['version']!=1:return fallback
    try:
        d=copy.deepcopy(raw)
        for key in ('season','tracked_since'):
            if not integer(d[key],9999) or d[key]<1900:raise ValueError()
        if d['season']!=season or d['tracked_since']>season:raise ValueError()
        for key in ('season_goals','season_matches','career_goals','career_matches','sessions','transfers','minutes'):
            if not integer(d[key],1_000_000_000):raise ValueError()
        if d['career_goals']<d['season_goals'] or d['career_matches']<d['season_matches']:raise ValueError()
        for key in ('trust','peak_trust'):
            if not integer(d[key],100):raise ValueError()
        if d['peak_trust']<d['trust']:raise ValueError()
        if type(d['last_change'])is not int or not -100<=d['last_change']<=100:raise ValueError()
        if not integer(d['last_minutes'],90) or d['last_role']not in ROLES:raise ValueError()
        if not integer(d['goal_target'],30) or d['goal_target']<3:raise ValueError()
        if not isinstance(d['club'],str) or len(d['club'])>64 or d['club'] and not d['club'].isprintable():raise ValueError()
        if d['focus']not in FOCI or set(d['skills'])!=set(FOCI):raise ValueError()
        for skill in d['skills'].values():
            if set(skill)!={'level','xp'} or not integer(skill['level'],10) or not integer(skill['xp'],needed(skill['level'])-1) or skill['level']==10 and skill['xp']!=0:raise ValueError()
        session=d['session']
        if session is not None:
            if set(session)!={'id','focus','on_focus','rewarded'} or not integer(session['id'],d['sessions']) or session['id']==0 or session['focus']not in FOCI or not integer(session['on_focus'],3) or type(session['rewarded'])is not bool:raise ValueError()
        if not isinstance(d['season_earned'],list) or len(d['season_earned'])>3 or len(set(d['season_earned']))!=len(d['season_earned']) or not set(d['season_earned'])<={'goals','trust','top3'}:raise ValueError()
        if not isinstance(d['archive'],list) or len(d['archive'])>20:raise ValueError()
        seen=set()
        for row in d['archive']:
            if set(row)!={'season','goals','target','earned'} or not integer(row['season'],9999) or not d['tracked_since']<=row['season']<=season or row['season']in seen or not integer(row['goals'],1_000_000_000) or not integer(row['target'],30):raise ValueError()
            if not isinstance(row['earned'],list) or len(row['earned'])>3 or not set(row['earned'])<={'goals','trust','top3'}:raise ValueError()
            seen.add(row['season'])
        return {key:d[key] for key in fallback}
    except (KeyError,ValueError,TypeError,AttributeError):return fallback

class DevelopmentCareer:
    def _development_target(self):
        rounds=self.current_league.total_rounds
        tier=self.club.tier if self.club else self.current_league.tier
        previous=self.development['archive'][-1]['goals'] if self.development['archive'] else 0
        return min(18,max(5,round(rounds*(.30 if tier==1 else .25)),min(18,round(previous*.8))))

    def _ensure_development(self):
        d=self.development
        if d['season']!=self.season:
            d.update(season=self.season,season_goals=0,season_matches=0,season_earned=[],peak_trust=d['trust'],session=None)
            d['goal_target']=self._development_target()
        uid=self.club.uid if self.club else ''
        if uid!=d['club']:
            initial_binding=not d['club'] and not d['archive'] and not d['transfers']
            d.update(club=uid,trust=50,last_change=0,last_minutes=0,last_role='Starter')
            d['peak_trust']=max(d['peak_trust'],50)
            if initial_binding or d['season_matches']==0:d['goal_target']=self._development_target()
        return d

    @property
    def coach_trust(self):return self._ensure_development()['trust']
    @property
    def team_role(self):
        if not self.club:return 'Free agent'
        trust=self.coach_trust
        return 'Substitute' if trust<45 else 'Key player' if trust>=80 else 'Starter'
    @property
    def training_focus(self):
        d=self._ensure_development()
        return d['session']['focus'] if d['session'] is not None else d['focus']

    def choose_training_focus(self,focus):
        if focus not in FOCI:return False
        if self.training_used_this_week:
            self.message='Finish the next match before changing focus.';return False
        before=copy.deepcopy(self.development);self._ensure_development()['focus']=focus
        if self.save() is False:
            self.development=before;return False
        return True

    def _reserve_development_training(self):
        d=self._ensure_development()
        if d['session'] is None:
            d['sessions']+=1
            d['session']=dict(id=d['sessions'],focus=d['focus'],on_focus=0,rewarded=False)

    def _reward_development_training(self):
        d=self._ensure_development();session=d['session']
        if session is None or session['rewarded']:return
        session['rewarded']=True
        skill=d['skills'][session['focus']]
        if skill['level']<10:
            skill['xp']+=12+4*session['on_focus']
            while skill['level']<10 and skill['xp']>=needed(skill['level']):
                skill['xp']-=needed(skill['level']);skill['level']+=1
            if skill['level']==10:skill['xp']=0
        d['trust']=min(100,d['trust']+2);d['peak_trust']=max(d['peak_trust'],d['trust'])
        self._recognise_development()

    def _recognise_development(self):
        d=self._ensure_development()
        for key,met in (('goals',d['season_goals']>=d['goal_target']),('trust',d['peak_trust']>=70)):
            if met and key not in d['season_earned']:d['season_earned'].append(key)

    def playing_window(self,international=False,key_match=False):
        if international:return 0,90
        if not self.club:return 0,0
        trust=self.coach_trust
        if trust<45:return 60,90
        return (0,90) if trust>=60 or key_match else (0,75)

    @property
    def opportunity_role_bonus(self):
        return -.25 if self.team_role=='Substitute' else .25 if self.team_role=='Key player' else 0.

    def record_development_match(self,goals,misses,key_match=False):
        d=self._ensure_development();entry,exit=self.playing_window(key_match=key_match)
        d['last_minutes']=exit-entry;d['last_role']=self.team_role;d['minutes']+=exit-entry
        before=d['trust']
        change=min(12,goals*6)+(2 if goals and key_match else 0) if goals else (-4 if misses>=3 else -3 if misses else -1)
        d['trust']=max(0,min(100,before+change));d['last_change']=d['trust']-before
        d['peak_trust']=max(d['peak_trust'],d['trust'])
        d['season_goals']+=goals;d['season_matches']+=1;d['career_goals']+=goals;d['career_matches']+=1
        self._recognise_development()

    def finish_development_season(self):
        d=self._ensure_development();self._recognise_development()
        goals=self.current_league.scorer_goals.get(self.player_name,0)
        rank=1+sum(g>goals for name,g in self.current_league.scorer_goals.items() if name!=self.player_name)
        if goals>0 and rank<=3 and d['season_matches']>0 and 'top3'not in d['season_earned']:d['season_earned'].append('top3')
        if not any(r['season']==self.season for r in d['archive']):
            d['archive']=(d['archive']+[dict(season=self.season,goals=d['season_goals'],target=d['goal_target'],earned=list(d['season_earned']))])[-20:]

    def skill_level(self,focus):return self._ensure_development()['skills'][focus]['level']

    def finishing_controls(self,shot_type):
        if shot_type=='header':
            level=self.skill_level('heading');return level*.1,1.-level*.008
        if shot_type=='penalty':
            level=self.skill_level('penalties');return level*.08,1.-level*.008
        return (0.,1.-self.skill_level('placed')*.012) if shot_type=='kick' else (0.,1.)

    def low_finish_speed(self,shot_type,height):
        return 1.+self.skill_level('low')*.006 if shot_type=='kick' and height<=.9 else 1.
