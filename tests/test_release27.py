import json,unittest
from pathlib import Path
from unittest.mock import patch
from game_timing import simulation_dt
from goal_nets import COIMBRA_PRETO_UID,ROUNDED_STYLE,for_stadium,stadium_style
from shot_trajectory import OPPORTUNITY_BALL_SPEED,opportunity_velocity,launch_velocity
from types import SimpleNamespace

class BallSpeedAndHomeNet(unittest.TestCase):
 def test_only_player_shot_uses_faster_flight_solver(self):
  start=(1.,18.,.115);target=(2.,1.);duration=.9
  with patch('shot_trajectory.launch_velocity',return_value=(1,2,3))as solver:
   self.assertEqual(opportunity_velocity(start,target,duration),(1,2,3))
   solver.assert_called_once_with(start,target,duration/1.05)
  self.assertEqual(OPPORTUNITY_BALL_SPEED,1.05)
  self.assertLess(opportunity_velocity(start,target,duration)[1],launch_velocity(start,target,duration)[1])
 def test_all_other_clocks_stay_real_time(self):
  for view in ('shot','match','hub','splash'):
   self.assertAlmostEqual(sum(simulation_dt(1/60,view)for _ in range(60)),1.)
 def test_coimbra_identity_and_home_training_away_assignment(self):
  names=json.loads(Path('assets/data/fictional_names.json').read_text())
  def find(o):
   if isinstance(o,dict):
    if COIMBRA_PRETO_UID in o:return o[COIMBRA_PRETO_UID]
    for v in o.values():
     found=find(v)
     if found:return found
  self.assertEqual(find(names)['name'],'Coimbra Preto')
  self.assertEqual(for_stadium(COIMBRA_PRETO_UID),ROUNDED_STYLE)
  club=SimpleNamespace(uid=COIMBRA_PRETO_UID,name='Custom name')
  g=SimpleNamespace(career=SimpleNamespace(club=club),match_home=None,shot_context='training')
  self.assertEqual(stadium_style(g),ROUNDED_STYLE)
  g.shot_context='match';g.match_home=club;self.assertEqual(stadium_style(g),ROUNDED_STYLE)
  other=next(str(i)for i in range(100)if for_stadium(str(i))!=ROUNDED_STYLE)
  g.match_home=SimpleNamespace(uid=other);self.assertEqual(stadium_style(g),for_stadium(other))
