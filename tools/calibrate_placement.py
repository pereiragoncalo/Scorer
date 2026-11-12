"""Paired physical corner finishes; exact aim is not human conversion."""
import sys,random,json
from pathlib import Path
from collections import Counter
from contextlib import nullcontext
import argparse
sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parents[1]/"ui_tests")]
from unittest.mock import patch
from test_menus import isolated_game
from test_retro_attendance_titles import RetroSceneTests
from career import PHYSICS_STEP
from kivy.clock import Clock
parser=argparse.ArgumentParser();parser.add_argument("--samples",type=int,default=50);parser.add_argument("--output",type=Path,required=True);args=parser.parse_args()
if not 1<=args.samples<=1000:parser.error("samples must be1–1000")
rows=[]
with patch('edition.WORLD_BUILD',True),isolated_game() as g:
 c=RetroSceneTests().prepare(g);Clock.unschedule(g.update);g.draw=lambda:None
 for tier in (1,4):
  c.club.tier=tier;opponent=g.match_away if g.match_home.uid==c.club.uid else g.match_home;opponent.tier=tier
  for kind in ('first_time','long_shot'):
   for mode in ('previous','tuned'):
    counts=Counter()
    for seed in range(args.samples):
     random.seed(39000+seed);c.rng.seed(67000+seed);g.elapsed=0;g.match_player_goals=0;g.match_home_score=g.match_away_score=0
     g.current_chance_difficulty='hard';g._prepare_next_shot();g._start_opportunity(kind,seed);g._update_buildup(g.current_opportunity.duration);g.power=.85
     x=(3.2 if seed%2 else -3.2);z=(.35 if seed%4<2 else 2.1)
     scope=patch('finishing_balance.placed_keeper_balance',return_value=(0.,1.,0.)) if mode=='previous' else nullcontext()
     with scope,patch.object(g,'_play_goal_crowd_sound'):
      g.shoot(x,z)
      for _ in range(int(8/PHYSICS_STEP)):
       g.elapsed+=PHYSICS_STEP;g.state_age+=PHYSICS_STEP;g._update_goalkeeper_shot(PHYSICS_STEP);g._update_ball(PHYSICS_STEP)
       if g.outcome_registered:break
     counts[g.result_text if g.outcome_registered else 'UNRESOLVED']+=1
    row=dict(tier=tier,kind=kind,mode=mode,samples=args.samples,outcomes=dict(counts));rows.append(row);print(row,flush=True)
args.output.write_text(json.dumps(dict(method='Paired exact corner targets, same seeds. Physical outcomes only; not human conversion.',rows=rows),indent=2)+'\n')
