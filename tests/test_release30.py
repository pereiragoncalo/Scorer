import math,unittest
from types import SimpleNamespace
from defensive_pressure import Pressure,advance
from net_drape import RollingReplay,MATERIALS,ReferenceCloth
from net_cloth import NetGeometry
from net_presentation import advance as advance_net

class SmallDefensiveStep(unittest.TestCase):
 def test_defender_takes_one_step_then_idles_with_space_to_shoot(self):
  actor=object();p=Pressure(actor,(0.,8.))
  g=SimpleNamespace(_pressure=p,outcome_registered=False,state='aim',STATE_BUILDUP='build',STATE_AIMING='aim',STATE_SHOT='shot',current_opportunity=SimpleNamespace(kind='long_shot'),aim_x=0.,shot_origin_x=0.,shot_origin_y=18.,shot_type='normal')
  for _ in range(120):advance(g,1/60)
  self.assertLessEqual(math.dist(p.position,p.origin),.900001)
  self.assertGreater(math.dist(p.position,(0.,18.)),3.)
  self.assertFalse(p.moving)
 def test_close_defender_holds_instead_of_crowding_and_wall_waits(self):
  p=Pressure(object(),(0.,16.))
  g=SimpleNamespace(_pressure=p,outcome_registered=False,state='aim',STATE_BUILDUP='build',STATE_AIMING='aim',STATE_SHOT='shot',current_opportunity=SimpleNamespace(kind='long_shot'),aim_x=0.,shot_origin_x=0.,shot_origin_y=18.,shot_type='normal')
  for _ in range(120):advance(g,.1)
  self.assertEqual(p.position,p.origin);self.assertFalse(p.moving)
  g.current_opportunity.kind='free_kick';p.position=(0.,8.);p.origin=p.position;advance(g,.5);self.assertEqual(p.position,p.origin)

class OccupiedRoundedPocket(unittest.TestCase):
 def test_low_high_and_oblique_shots_settle_in_the_rear_mesh_without_energy_gain(self):
  for height,speed,vx,x in ((.115,25,0,0),(1.,25,0,0),(2.,35,0,0),(1.,25,-4,-2.8),(.4,15,3,2.5),(2.1,20,-6,-2.8),(2.1,20,6,2.8)):
   with self.subTest(height=height,vx=vx):
    r=RollingReplay('rounded',height=height,geometry=NetGeometry('rounded',depth=3.5),coarse=True)
    r.position=[x,-.02,height];r.velocity=[vx,-speed,0.];r.ball=tuple(r.position)
    anchors=[r.cloth.positions[i][:]for i in r.ground_anchors];ties=tuple(t[1]for t in r.cloth.tethers)
    for _ in range(720):
     energy=sum(v*v for v in r.velocity)+19.62*r.ball[2];r.one_step()
     self.assertLessEqual(sum(v*v for v in r.velocity)+19.62*r.ball[2],energy+1e-6)
     if r.cloth.retain_pocket:self.assertLessEqual(r.velocity[1],1e-8)
    self.assertLess(r.ball[1],-1.7 if abs(vx)==6 else -2.1);self.assertAlmostEqual(r.ball[2],r.radius,places=5)
    self.assertLess(math.sqrt(sum(v*v for v in r.velocity)),.05)
    self.assertTrue(r.cloth.retain_pocket)
    self.assertEqual([r.cloth.positions[i]for i in r.ground_anchors],anchors)
    self.assertEqual(tuple(t[1]for t in r.cloth.tethers),ties)
 def test_pocket_releases_on_collection_and_reset_does_not_create_a_permanent_bulge(self):
  c=ReferenceCloth(NetGeometry('rounded',depth=3.5),MATERIALS['rounded'].config,coarse=True)
  original=[p[:]for p in c.rest];c.retain_pocket=True
  game=SimpleNamespace(_net_cloth=c,_net_replay=SimpleNamespace(collected=True))
  advance_net(game,.1);self.assertFalse(c.retain_pocket);self.assertEqual(c.rest,original)
  c.retain_pocket=True;c.reset();self.assertFalse(c.retain_pocket);self.assertEqual(c.positions,original)
