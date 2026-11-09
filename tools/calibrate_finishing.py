"""Paired physical finishing check. Exact targets isolate keeper tuning, not human conversion."""
import sys,random,json,argparse
from pathlib import Path
from collections import Counter
from unittest.mock import patch
sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parents[1]/'ui_tests')]
from test_menus import isolated_game
import test_retro_attendance_titles as retro
from finishing_balance import NEUTRAL
from career import PHYSICS_STEP,HEADER_BALL_HEIGHT
from kivy.clock import Clock

def experiment(samples):
 rows=[]
 with patch('edition.WORLD_BUILD',True),isolated_game() as g:
  c=retro.RetroSceneTests().prepare(g);Clock.unschedule(g.update);g.draw=lambda:None
  normal=g._finishing_balance
  for tier in (1,4):
   c.club.tier=tier
   opponent=g.match_away if g.match_home.uid==c.club.uid else g.match_home
   opponent.tier=tier
   for kind in ('penalty','through_ball','header_close','header_far','first_time'):
    for mode in ('previous','tuned'):
     counts=Counter()
     for seed in range(samples):
      random.seed(39000+seed);c.rng.seed(67000+seed);g.elapsed=0;g.match_player_goals=0;g.match_home_score=g.match_away_score=0
      g._finishing_balance=(lambda:NEUTRAL) if mode=='previous' else normal
      g.shot_time_limit,g.current_aim_speed=c.difficulty_profile(False);g.current_chance_difficulty='hard';g._prepare_next_shot()
      g._start_opportunity('cross' if kind.startswith('header') else kind,seed);g._update_buildup(g.current_opportunity.duration) if g.current_opportunity.duration else None
      if kind.startswith('header'):
       g.shot_origin_x=1.5 if seed%2 else -1.5;g.shot_origin_y=7. if kind=='header_close' else 12.;g.ball.reset(g.shot_origin_x,g.shot_origin_y,HEADER_BALL_HEIGHT)
      target=random.Random(98000+seed);x,z=target.uniform(-3.25,3.25),target.uniform(.25,2.20);g.power=.85
      with patch.object(g,'_play_goal_crowd_sound'):
       g.shoot(x,z)
       for _ in range(int(8/PHYSICS_STEP)):
        g.elapsed+=PHYSICS_STEP;g.state_age+=PHYSICS_STEP;g._update_goalkeeper_shot(PHYSICS_STEP);g._update_ball(PHYSICS_STEP)
        if g.outcome_registered:break
      counts[g.result_text if g.outcome_registered else 'UNRESOLVED']+=1
     row=dict(tier=tier,kind=kind,mode=mode,samples=samples,outcomes=dict(counts),conversion=counts['GOAL!']/samples);rows.append(row);print(row,flush=True)
  g._finishing_balance=normal
 return dict(method=__doc__,rows=rows)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--samples',type=int,default=60);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.write_text(json.dumps(experiment(a.samples),indent=2)+'\n')
