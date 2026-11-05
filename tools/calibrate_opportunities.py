import sys,os,json,tempfile,random
from collections import Counter
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from main import StrikerGame,PHYSICS_STEP
from kivy.clock import Clock
from opportunity_sequences import KINDS
import argparse
p=argparse.ArgumentParser(description='Paired physical opportunity calibration; exact targets bypass human timing.')
p.add_argument('--samples',type=int,default=80);p.add_argument('--output',type=Path,required=True)
p.add_argument('--kinds',nargs='+',default=['baseline',*KINDS],choices=['baseline',*KINDS]);args=p.parse_args()
if not 1<=args.samples<=1000:p.error('samples must be between 1 and 1000')
rows=[]
with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,STRIKER_SAVE_DIR=t),patch('edition.WORLD_BUILD',True),patch('analytics_config.ENDPOINT',''),patch('online_config.ORIGIN',''),patch('anonymous_stats.APP_STATS_MANDATORY',False):
 g=StrikerGame();Clock.unschedule(g.update);g.draw=lambda:None;g.size=(1280,591);g.career.accept_starting_offer(g.career.offers[0]);g.view='shot';g.shot_context='match'
 for tier in (1,2):
  g.career.club.tier=tier
  for kind in args.kinds:
   for strategy in ('uniform','low_corners','high_corners'):
    outcomes=Counter()
    for seed in range(args.samples):
     random.seed(39000+seed);g.career.rng.seed(67000+seed);g.elapsed=0;g.current_chance_difficulty='hard';g._prepare_next_shot();g.shot_time_limit=4.
     if kind!='baseline':g._start_opportunity(kind,seed);g._update_buildup(g.current_opportunity.duration)
     g.power=.85
     target=random.Random(98000+seed);x,z=target.uniform(-3.25,3.25),target.uniform(.25,2.20)
     if strategy!='uniform':x,z=(3.25 if seed%2 else -3.25),(.30 if strategy=='low_corners' else 2.15)
     with patch.object(g,'_play_goal_crowd_sound'):
      g.shoot(x,z)
      for _ in range(int(10/PHYSICS_STEP)):
       g.elapsed+=PHYSICS_STEP;g.state_age+=PHYSICS_STEP;g._update_goalkeeper_shot(PHYSICS_STEP);g._update_ball(PHYSICS_STEP)
       if g.outcome_registered:break
     outcomes[g.result_text if g.outcome_registered else 'UNRESOLVED']+=1
    rows.append(dict(tier=tier,kind=kind,strategy=strategy,samples=args.samples,outcomes=dict(outcomes),conversion=outcomes['GOAL!']/args.samples));print(rows[-1],flush=True)
args.output.write_text(json.dumps(dict(method='Paired physical shots with exact aim, bypassing human aim/timer. Not human conversion or guaranteed results.',rows=rows),indent=2)+'\n')
