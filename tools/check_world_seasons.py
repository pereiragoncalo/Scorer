"""Three-year World lifecycle check with controlled scores, not a human playtest."""
import json,os,random,sys,tempfile,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from career import CareerMode
class TestAccess:
    def has_world_access(self):return True

def check():
    random.seed(902026)
    with tempfile.TemporaryDirectory() as directory:
        previous=os.environ.get('STRIKER_SAVE_DIR');os.environ['STRIKER_SAVE_DIR']=directory
        try:
            c=CareerMode(TestAccess(),autoload=False,starter_country='Brazil',save_slot='world');c.league_key='Brazil|1';c.club_name=max(c.current_league.clubs,key=lambda x:x.rating).name;c.nationality='Argentina';c.morale=19
            start=time.monotonic();counts={};seen=set();dates=[];checkpoints=0
            for n in range(600):
                kind,h,a=c.next_match()
                if c.season>=2029:break
                identity=(c.season,kind,c.current_league.round_index if kind=='league' else 0)
                assert identity not in seen,'Repeated fixture';seen.add(identity)
                actor='nation:'+c.nationality if h.uid.startswith('nation:') else c.club.uid
                score=(2,0) if h.uid==actor else (0,2)
                c.finish_match(h,a,1,0,forced_score=score,competition=kind)
                dates.append(c.fixture_history[-1]['date']);assert dates==sorted(dates),'Calendar moved backwards'
                key=kind.split('|')[1] if kind.startswith('world|') else kind;counts[key]=counts.get(key,0)+1
                if n%17==0:
                    assert c.save();restored=CareerMode(TestAccess(),save_slot='world');assert restored.club_name and restored.season==c.season
                    assert restored.world_competitions.to_dict()==c.world_competitions.to_dict();c=restored;checkpoints+=1
            assert c.season==2029
            return dict(method='Seeded engine lifecycle with controlled player-team scores; not physical or human Android play.',seed=902026,season=c.season,completed_matches=n,types=counts,reloads=checkpoints,archived_seasons=len(c.competition_archive),seconds=round(time.monotonic()-start,2),caps=c.international_caps,international_goals=c.international_goals,calendar_nondecreasing=True,repeated_fixtures=False)
        finally:
            if previous is None:os.environ.pop('STRIKER_SAVE_DIR',None)
            else:os.environ['STRIKER_SAVE_DIR']=previous
if __name__=='__main__':print(json.dumps(check(),indent=2))
