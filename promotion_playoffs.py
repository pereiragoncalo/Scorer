"""Persistent ranked promotion/relegation ties, including mixed-division finals."""
import copy
from world_competitions import Tournament, rng_for

class PlayoffTournament(Tournament):
    def __init__(self,key,title,teams,seed,plan,*,start_week,ranks=None):
        super().__init__(key,title,teams,seed,kind='knockout',start_week=start_week,seeded=True)
        self.kind='promotion';self.fixtures=[];self.active=[];self.champion='';self.stage_number=0
        self.plan=copy.deepcopy(plan);self.results={};self.ranks=dict(ranks or {});self.last_week=start_week-1
        self._draw_round()

    def _resolve(self,ref):
        if ref.startswith('win:'):return self.results[ref[4:]]
        if ref.startswith('lose:'):
            f=next(f for f in self.fixtures if f['tie']==ref[5:]);return next(uid for uid in (f['home'],f['away']) if uid!=self.results[ref[5:]])
        return ref

    def _draw_round(self):
        self.active=[];self.stage_number+=1
        games=self.plan[self.stage_number-1];self.stage=games[0].get('title','Promotion/relegation playoff')
        start=self.last_week+1
        for game in games:
            home,away=self._resolve(game['home']),self._resolve(game['away'])
            if game.get('seed_second') and self.ranks.get(home,999)<self.ranks.get(away,999):home,away=away,home
            if home==away:raise ValueError('A playoff club cannot play itself')
            f=self._add(home,away,start,tie=game['id']);f['stage']=game.get('title',self.stage)
            if game.get('neutral'):f['neutral']=True
            if game.get('legs',1)==2:
                f=self._add(away,home,start+1,tie=game['id'],leg=2);f['stage']=game.get('title',self.stage)
        self.last_week=max(f['week'] for f in self.fixtures if f['id'] in self.active)

    def _progress(self):
        for game in self.plan[self.stage_number-1]:
            legs=[f for f in self.fixtures if f['id'] in self.active and f['tie']==game['id']]
            a,b=legs[0]['home'],legs[0]['away'];total={a:0,b:0}
            for f in legs:
                total[f['home']]+=f['score'][0];total[f['away']]+=f['score'][1]
            policy=game.get('decision','extra_pens');last=legs[-1]
            if policy=='rank' and self.key.startswith('playoff:Italy:') and game['id']=='final':
                points={t['uid']:t.get('points',0) for t in self.teams.values()}
                if points[a]==points[b]:policy='extra_pens'
            if total[a]==total[b] and policy.startswith('extra_'):
                from career import poisson_goal,realistic_goal_means
                rng=rng_for(self.seed,self.key,game['id'],'extra-time');means=realistic_goal_means(self.teams[last['home']]['rating'],self.teams[last['away']]['rating'])
                extra=[poisson_goal(rng,m/3) for m in means];last['extra_time']=extra
                for i,uid in enumerate((last['home'],last['away'])):last['score'][i]+=extra[i];total[uid]+=extra[i]
            if total[a]!=total[b]:winner=max(total,key=total.get)
            elif policy.endswith('rank'):
                winner=min((a,b),key=lambda uid:(self.ranks.get(uid,999),uid))
            else:
                rng=rng_for(self.seed,self.key,game['id'],'penalties');winner=rng.choice([a,b])
                last['penalties']=[5,4] if last['home']==winner else [4,5]
            self.results[game['id']]=winner
            for f in legs:f['winner']=winner
        if self.stage_number==len(self.plan):
            self.qualified=list(dict.fromkeys([self.results[g['id']] for games in self.plan for g in games if g.get('qualifies')]+[self.results[g['id']] for g in self.plan[-1]]));self.champion=self.qualified[0];self.stage='Completed';self.active=[]
        else:self._draw_round()

    @classmethod
    def from_dict(cls,data):
        extra={'plan','results','ranks'}
        if not extra<=set(data):raise ValueError('Missing playoff bracket')
        base=copy.deepcopy(data)
        for k in extra:base.pop(k)
        base['kind']='knockout';validated=Tournament.from_dict(base)
        obj=object.__new__(cls);obj.__dict__=copy.deepcopy(data)
        if not isinstance(obj.plan,list) or not 1<=len(obj.plan)<=8 or not isinstance(obj.results,dict) or not isinstance(obj.ranks,dict):raise ValueError('Invalid playoff bracket')
        refs=set(obj.teams);seen=set()
        for games in obj.plan:
            if not isinstance(games,list) or not 1<=len(games)<=16:raise ValueError('Invalid playoff round')
            new=set()
            for g in games:
                if not isinstance(g,dict) or not {'id','home','away'}<=set(g) or set(g)-{'id','home','away','legs','decision','title','qualifies','neutral','seed_second'}:raise ValueError('Invalid playoff tie')
                if not isinstance(g['id'],str) or g['id'] in seen or g['home'] not in refs or g['away'] not in refs or g['home']==g['away'] or g.get('legs',1) not in (1,2) or g.get('decision','extra_pens') not in ('extra_pens','extra_rank','rank','pens') or type(g.get('qualifies',False))is not bool or type(g.get('neutral',False))is not bool or type(g.get('seed_second',False))is not bool:raise ValueError('Invalid playoff references')
                new.add(g['id'])
            seen|=new;refs|={prefix+k for k in new for prefix in ('win:','lose:')}
        if not set(obj.results)<=seen or not set(obj.results.values())<=set(obj.teams) or any(uid not in obj.teams or type(rank)is not int for uid,rank in obj.ranks.items()):raise ValueError('Invalid playoff winners')
        if not 1<=obj.stage_number<=len(obj.plan):raise ValueError('Invalid playoff progress')
        for key,winner in obj.results.items():
            fixtures=[f for f in obj.fixtures if f['tie']==key]
            if not fixtures or any(winner not in (f['home'],f['away']) or f['winner']!=winner for f in fixtures):raise ValueError('Playoff winner differs from played tie')
        if obj.champion and (obj.active or not obj.qualified or obj.champion!=obj.qualified[0] or obj.stage_number!=len(obj.plan)):raise ValueError('Invalid playoff completion')
        return obj
