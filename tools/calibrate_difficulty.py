"""Paired seeded physical shots and synthetic seasons; never a human/device test."""
import argparse,json,os,random,sys,tempfile
from collections import Counter
from pathlib import Path
from unittest.mock import patch
os.environ.setdefault('KIVY_NO_ARGS','1');sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from main import StrikerGame,PHYSICS_STEP
from kivy.clock import Clock
from kivy.core.window import Window

def experiment(samples=100):
    rows=[];old=random.getstate()
    with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,STRIKER_SAVE_DIR=t),patch('edition.WORLD_BUILD',True),patch('analytics_config.ENDPOINT',''),patch('online_config.ORIGIN',''):
        g=StrikerGame();Clock.unschedule(g.update);g.draw=lambda:None;g.size=(960,540);g.career.accept_starting_offer(g.career.offers[0]);g.shot_context='match';g.view='shot'
        try:
            for tier in (5,4,3,2,1):
                g.career.club.tier=tier
                for strategy in ('uniform','corners','low_corners','placed'):
                    for kind in ('easy','hard'):
                        outcomes=Counter()
                        for seed in range(samples):
                            random.seed(39000+seed);g.career.rng.seed(67000+seed);g.elapsed=0;g.current_chance_difficulty=kind;g._prepare_next_shot();g.power=.85
                            target=random.Random(98000+seed)
                            x,z=(target.uniform(-3.25,3.25),target.uniform(.25,2.20))
                            if strategy in ('corners','low_corners'):x,z=(3.45 if seed%2 else -3.45),(2.25 if strategy=='corners' else .30)
                            if strategy=='placed':x,z=(1 if seed%2 else -1)*target.uniform(2.65,3.45),target.uniform(.25,2.25)
                            with patch.object(g,'_play_goal_crowd_sound'):
                                g.shoot(x,z)
                                for _ in range(int(15/PHYSICS_STEP)):
                                    g.elapsed+=PHYSICS_STEP;g.state_age+=PHYSICS_STEP;g._update_goalkeeper_shot(PHYSICS_STEP);g._update_ball(PHYSICS_STEP)
                                    if g.outcome_registered:break
                            outcomes[g.result_text if g.outcome_registered else 'UNRESOLVED']+=1
                        row=dict(tier=tier,strategy=strategy,chance=kind,samples=samples,outcomes=dict(outcomes),conversion=outcomes['GOAL!']/samples);rows.append(row)
        finally:Window.unbind(on_key_down=g._on_key_down);random.setstate(old)
    return {'method':'Paired exact targets bypass aim/timer. Corners are an idealised upper-skill stress test, not human conversion or a scoring guarantee. No count uploads or user career writes.','rows':rows}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--samples',type=int,default=100);p.add_argument('--output',type=Path,required=True);a=p.parse_args();result=experiment(a.samples);a.output.write_text(json.dumps(result,indent=2)+'\n');print('Saved',a.output)
