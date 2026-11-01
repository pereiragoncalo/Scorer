"""Synthetic 38-match projection from measured physical conversions, not human play."""
import argparse,json,os,random,sys,tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from career import CareerMode,CareerClub

def project(measurements,seasons=2000,matches=38):
    pairs={(r['tier'],r['strategy'],r['chance']):r['conversion'] for r in measurements['rows']};result=[]
    with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,STRIKER_SAVE_DIR=t):
        c=CareerMode(autoload=False);c.morale=c.stamina=20;c.last_training_week=c.week;c.training_session_week=c.week;c.training_session_goals=3
        for tier,strategy in sorted({(r['tier'],r['strategy']) for r in measurements['rows']}):
            p_easy=pairs[tier,strategy,'easy'];p_hard=pairs[tier,strategy,'hard'];rng=random.Random(488000+tier)
            # Match the game's tier-rating centres; no early-table rank bonus.
            clear=[]
            for _ in range(128):
                opponent=CareerClub('Calibration','Calibration','Test',tier,88-(tier-1)*8+rng.uniform(-7,7))
                profile=c.opponent_chance_profile(opponent);assert c.chance_count(opponent)==3
                clear.append(profile.clear_chance_probability)
            totals=[]
            for _ in range(seasons):
                goals=0
                for _ in range(matches):
                    easy=rng.random()<rng.choice(clear)
                    goals+=sum(rng.random()<(p_easy if easy and n==0 else p_hard) for n in range(3))
                totals.append(goals)
            totals.sort();result.append(dict(tier=tier,strategy=strategy,seasons=seasons,matches_per_season=matches,mean_goals_per_match=sum(totals)/(seasons*matches),share_seasons_above_one_goal_per_match=sum(n>matches for n in totals)/seasons,season_goals_p95=totals[int(.95*(seasons-1))]))
    return {'method':'Synthetic independent outcomes sampled from physical shot conversion measurements. Maximum morale/stamina, trained with three training goals, three opportunities every match, perfect requested targets and no timeouts. Not real human matches, not a forecast or a scoring cap. Seeded opponent ratings vary +/-7 around each tier centre; no table/form updates.','rows':result}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('measurements',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.write_text(json.dumps(project(json.loads(a.measurements.read_text())),indent=2)+'\n');print('Saved',a.output)
