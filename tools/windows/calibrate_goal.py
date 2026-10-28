"""Paired seeded physical shots into each profile's goal. Not a human skill test."""
import argparse
from collections import Counter
import json,os,random,sys,tempfile
from pathlib import Path
from unittest.mock import patch
os.environ.setdefault('KIVY_NO_ARGS','1')
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from main import StrikerGame,PHYSICS_STEP
from kivy.clock import Clock
from kivy.core.window import Window


def experiment(samples):
    previous=random.getstate();rows={}
    try:
        for desktop in (False,True):
            with tempfile.TemporaryDirectory() as directory,patch.dict(os.environ,STRIKER_SAVE_DIR=directory),patch('release_settings.DESKTOP_WINDOWS',desktop,create=True):
                g=StrikerGame();Clock.unschedule(g.update);g.draw=lambda:None;g.size=(1280,720)
                outcomes=Counter()
                try:
                    for seed in range(samples):
                        random.seed(39000+seed);g.career.rng.seed(67000+seed)
                        g.career.morale=g.career.stamina=10;g.shot_context='match';g.view='shot'
                        g.current_chance_difficulty='hard';g._prepare_next_shot();g.power=.85
                        target=random.Random(98000+seed)
                        x=target.uniform(-.94,.94)*g.goal_half_width;z=target.uniform(.14,.92)*g.goal_height
                        with patch.object(g,'_play_goal_crowd_sound'):
                            g.shoot(x,z)
                            for _ in range(int(15/PHYSICS_STEP)):
                                g.elapsed+=PHYSICS_STEP;g.state_age+=PHYSICS_STEP
                                g._update_goalkeeper_shot(PHYSICS_STEP);g._update_ball(PHYSICS_STEP)
                                if g.outcome_registered:break
                        outcomes[g.result_text if g.outcome_registered else 'UNRESOLVED']+=1
                    rows['windows' if desktop else 'original']={'samples':samples,'width':g.goal_width,'height':g.goal_height,'outcomes':dict(outcomes),'conversion':outcomes['GOAL!']/samples}
                finally:Window.unbind(on_key_down=g._on_key_down)
    finally:random.setstate(previous)
    return rows

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--samples',type=int,default=80);args=p.parse_args()
    if not 1<=args.samples<=512:p.error('samples must be1..512')
    print(json.dumps(experiment(args.samples),indent=2))
