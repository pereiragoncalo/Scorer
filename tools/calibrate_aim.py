"""Synthetic corner policy: perfect periodic anticipation vs 183ms response to stochastic aim; physical shots, not human measurements."""
import sys,os,json,math,random,tempfile
from pathlib import Path
from unittest.mock import patch
sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parents[1]/'ui_tests')]
from test_menus import isolated_game
from test_retro_attendance_titles import RetroSceneTests
from career import PHYSICS_STEP
from kivy.clock import Clock

def experiment(samples=60):
 rows=[]
 with patch('edition.WORLD_BUILD',True),isolated_game() as g:
  c=RetroSceneTests().prepare(g);Clock.unschedule(g.update);g.draw=lambda:None
  for mode,age in (('periodic-reference',18),('stochastic',18),('stochastic',42),('stochastic',46)):
   goals=timedout=shots=0
   for seed in range(samples):
    random.seed(seed+2700);c.rng.seed(seed+3700);c.last_training_week=c.week;c.season=c.life['start_season']+age-18;g.elapsed=0;g.match_player_goals=0;g.match_home_score=g.match_away_score=0;g.shot_time_limit,g.current_aim_speed=c.difficulty_profile(False)
    if seed%3:
     g.shot_time_limit=max(2.7,g.shot_time_limit*.78);g.current_aim_speed*=1.18
    g._prepare_next_shot();g._start_opportunity('through_ball' if seed%3==0 else ('long_cross' if seed%3==1 else 'first_time'),seed)
    g.state=g.STATE_AIMING;g.ball.x,g.ball.y,g.ball.z=g.current_opportunity.contact;g.frozen_scene_time=0;g.state_age=0
    if mode=='periodic-reference':g.shot_time_limit/=.40
    left=g.shot_time_limit;launched=False
    while left>0:
     dt=1/60;g.elapsed+=dt;g.state_age+=dt;left-=dt
     if mode=='periodic-reference':g.aim_phase+=dt*g.current_aim_speed*g.aim_direction;g._apply_aim_pattern()
     else:g._update_aim(dt)
     g._update_goalkeeper_idle(dt)
     # An ideal zero-latency player waits for an inside-post high/low corner.
     if 2.8<abs(g.aim_x)<3.55 and (g.aim_z>1.65 or g.aim_z<.6):
      if mode=='stochastic':
       for reaction in range(11):
        left-=1/60;g.elapsed+=1/60;g.state_age+=1/60;g._update_aim(1/60);g._update_goalkeeper_idle(1/60)
       if left<=0:break
      g.power=.85
      with patch.object(g,'_play_goal_crowd_sound'):g.shoot()
      launched=True;shots+=1;break
    if not launched:timedout+=1;continue
    for _ in range(int(8/PHYSICS_STEP)):
     g.elapsed+=PHYSICS_STEP;g.state_age+=PHYSICS_STEP;g._update_goalkeeper_shot(PHYSICS_STEP)
     with patch.object(g,'_play_goal_crowd_sound'):g._update_ball(PHYSICS_STEP)
     if g.outcome_registered:break
    goals+=g.result_text=='GOAL!'
   from career_life import decline
   representative_opportunities=round(3/decline(c))
   rows.append(dict(estimated_goals_with_age_quantity=max(1,representative_opportunities)*goals/samples,representative_opportunities=max(1,representative_opportunities),mode=mode,reaction_delay_seconds=0. if mode=='periodic-reference' else 11/60,age=age,opportunities=samples,shots=shots,goals=goals,timed_out_waiting=timedout,goals_per_three_chances=3*goals/samples))
 return dict(method=__doc__,rows=rows)
if __name__=='__main__':
 result=experiment();print(json.dumps(result,indent=2))
