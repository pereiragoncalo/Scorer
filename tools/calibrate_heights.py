"""Seeded actual shots by height; training and matches, no human/device claim."""
import argparse,json,os,random,sys,tempfile
from pathlib import Path
from collections import Counter
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));os.environ.setdefault('KIVY_NO_ARGS','1')
from main import StrikerGame,PHYSICS_STEP
from kivy.clock import Clock
from kivy.core.window import Window

def check(samples):
    rows=[]
    with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,STRIKER_SAVE_DIR=t),patch('edition.WORLD_BUILD',True),patch('analytics_config.ENDPOINT',''),patch('online_config.ORIGIN',''):
        g=StrikerGame();Clock.unschedule(g.update);g.draw=lambda:None;g.size=(960,540);g.career.accept_starting_offer(g.career.offers[0]);g.view='shot'
        try:
            for tier in (4,1):
                g.career.club.tier=tier
                for kind in ('training','easy','hard'):
                    if kind=='training' and tier==1:continue
                    for band,limits in [('low',(.25,.55)),('middle',(.9,1.5)),('high',(1.85,2.25))]:
                        outcomes=Counter()
                        for seed in range(samples):
                            random.seed(913000+seed);g.career.rng.seed(911000+seed);g.shot_context='training' if kind=='training' else 'match';g.current_chance_difficulty=kind;g.elapsed=0;g._prepare_next_shot()
                            target=random.Random(912000+seed);x=target.uniform(-3.25,3.25);z=target.uniform(*limits);g.power=target.uniform(.55,1.0)
                            with patch.object(g,'_play_goal_crowd_sound'):
                                g.shoot(x,z)
                                for _ in range(int(15/PHYSICS_STEP)):
                                    g.elapsed+=PHYSICS_STEP;g.state_age+=PHYSICS_STEP;g._update_goalkeeper_shot(PHYSICS_STEP);g._update_ball(PHYSICS_STEP)
                                    if g.outcome_registered:break
                            outcomes[g.result_text if g.outcome_registered else 'UNRESOLVED']+=1
                        rows.append(dict(tier=tier,context=kind,band=band,samples=samples,outcomes=dict(outcomes),conversion=outcomes['GOAL!']/samples))
        finally:Window.unbind(on_key_down=g._on_key_down)
    return {'method':'Real fixed-step shot/keeper/defender collisions, exact targets and varied power. Seeded comparison, not human scoring rates.','rows':rows}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--samples',type=int,default=120);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.write_text(json.dumps(check(a.samples),indent=2)+'\n');print('Saved',a.output)
