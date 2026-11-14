import math,random,unittest
from game_timing import GAME_SPEED,simulation_dt
from goal_nets import STYLES,ROUNDED_STYLE,for_stadium
from net_cloth import NetGeometry
from net_drape import MATERIALS,RollingReplay

class GameplaySpeed(unittest.TestCase):
 def test_gameplay_clock_is_exactly_five_percent_faster(self):
  for fps in (30,60,120):
   for view in ('shot','match'):
    self.assertAlmostEqual(sum(simulation_dt(1/fps,view)for _ in range(fps)),1.05)
   self.assertAlmostEqual(sum(simulation_dt(1/fps,'hub')for _ in range(fps)),1.)
  self.assertEqual(simulation_dt(-1,'shot'),0.)

class RoundedHexagonalNet(unittest.TestCase):
 def test_new_variant_preserves_all_old_types_and_stable_stadium_assignment(self):
  before=random.getstate();assigned={for_stadium(str(i))for i in range(100)}
  self.assertEqual(assigned,set(STYLES));self.assertEqual(len(STYLES),9)
  self.assertEqual(ROUNDED_STYLE.mesh,'hexagon');self.assertEqual(random.getstate(),before)
 def test_profile_and_floor_corners_are_curved_instead_of_rectangular(self):
  g=NetGeometry('rounded',depth=3.5)
  self.assertEqual(g.profile(0),(0.,g.height));self.assertAlmostEqual(g.profile(1)[0],-g.depth)
  for t in (.15,.4,.7):
   v=(g.top_depth+g.slope*t)/g.path;y,z=g.profile(v)
   self.assertAlmostEqual(((y+g.top_depth)/(g.touch-g.top_depth)+1)**2+(z/g.height-1)**2,1.)
   left=g.point('left',v,1);back=g.point('back',0,v)
   self.assertAlmostEqual(math.dist(left,back),0.,places=6)
  self.assertLess(abs(g.point('left',.8,0)[0]),g.width/2)
 def test_slack_and_deformation_capacity_exceed_double_existing_runtime_nets(self):
  old,new=MATERIALS['reference'].config,MATERIALS['rounded'].config
  self.assertGreaterEqual(new.net_slack,old.net_slack*2)
  self.assertGreaterEqual(new.net_max_stretch-1,(old.net_max_stretch-1)*2)
 def test_hanging_mesh_starts_still_and_has_welded_seams_ground_pins_and_three_ties(self):
  r=RollingReplay('rounded',height=1.,geometry=NetGeometry('rounded',depth=3.5),coarse=True);c=r.cloth
  self.assertEqual(c.displacement,0.);self.assertFalse(c.active);self.assertEqual(len(c.tethers),3)
  for side,column in (('left',0),('right',-1)):
   self.assertTrue(all(c.grids[side][2][-1][j]==c.grids['back'][2][j][column]for j in range(len(c.grids['back'][2]))))
  self.assertTrue(all(c.pinned[i]and c.positions[i]==c.rest[i]for i in r.ground_anchors))
 def test_folded_rounded_corner_regression_keeps_ball_inside_the_actual_net(self):
  r=RollingReplay('rounded',height=.2133531173,geometry=NetGeometry('rounded',depth=3.5),coarse=True)
  r.position=[-2.4793781671,-.02,.2133531173];r.velocity=[-15.7539256896,-28.4053528633,1.6112325425];r.ball=tuple(r.position)
  for _ in range(180):
   r.one_step();self.assertGreater(r.ball[1],-6.5)
   if r.ball[1]<-.02:self.assertTrue(r.mesh.inside(r.ball))
 def test_low_high_fast_and_oblique_shots_remain_retained_without_energy_gain(self):
  for height,speed,vx,x in ((.115,35.,0.,0.),(1.,25.,0.,0.),(2.1,35.,8.,2.8),(.4,40.,-14.,-2.8)):
   with self.subTest(height=height,speed=speed):
    r=RollingReplay('rounded',height=height,geometry=NetGeometry('rounded',depth=3.5),coarse=True)
    r.position=[x,-.02,height];r.velocity=[vx,-speed,0.];r.ball=tuple(r.position)
    for _ in range(240):
     energy=sum(v*v for v in r.velocity)+19.62*r.ball[2];r.one_step()
     self.assertLessEqual(sum(v*v for v in r.velocity)+19.62*r.ball[2],energy+1e-6)
     self.assertLessEqual(abs(r.ball[0]),r.geometry.width/2+3.)
     self.assertGreaterEqual(r.ball[1],-r.geometry.depth-3.)
     self.assertLess(r.ball[1],.01)
    self.assertTrue(r.hit);self.assertGreater(r.peak,.1)
