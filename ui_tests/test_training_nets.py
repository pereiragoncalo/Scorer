import math,unittest
from unittest.mock import patch
from kivy.core.window import Window
from kivy.graphics import Mesh
from test_menus import isolated_game,settle
from goal_nets import STYLES,NetStyle,for_stadium,lattice
from opportunity_sequences import TEXT,make_delivery
from training_opportunities import plan,BIB_KITS
from career import GOAL_DEPTH,PHYSICS_STEP

class TrainingNets(unittest.TestCase):
 def prepare(self,g):
  c=g.career
  if c.club is None:c.accept_starting_offer(c.offers[0])
  c.attend_coach_meeting();g._career_started=True
  return c
 def test_plan_resume_and_shared_deliveries_with_two_teams(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   c=self.prepare(g);g.draw=lambda:None;g.start_training()
   self.assertEqual(g._match_outfield_kits(),BIB_KITS)
   self.assertFalse(g._show_stadium_crowd())
   state=c.rng.getstate();first=plan(c);self.assertEqual(first,plan(c));self.assertEqual(state,c.rng.getstate())
   for focus in ('heading','penalties','low','placed'):
    c.development['focus']=focus
    c.development['session']['focus']=focus
    if focus=='heading':self.assertIn(plan(c)[0],('cross','long_cross','corner'))
    if focus=='penalties':self.assertEqual(plan(c)[0],'penalty')
   for kind in TEXT:
    g._prepare_next_shot();g._start_opportunity(kind,('test',kind))
    self.assertEqual(g.current_opportunity.kind,kind)
    self.assertEqual({p.team for p in g.field_players},{'attacker','defender'})
    actors=g.field_players+g.buildup_actors
    self.assertEqual(sum(p.team=='attacker' for p in actors)+1,5)
    self.assertEqual(sum(p.team=='defender' for p in actors)+1,5)
    expected=make_delivery(kind,('test',kind))
    self.assertIn(g.current_opportunity,(expected,expected.mirrored()))
    if expected.duration:g._update_buildup(expected.duration)
    self.assertEqual(g.state,g.STATE_AIMING)
    self.assertEqual(c.training_shots_taken,0)
   g._prepare_next_shot();original=g.current_opportunity
   g.view='training';g.start_training();self.assertEqual(g.current_opportunity,original)
   g.result_text='MISS!';g._advance_after_shot();self.assertEqual(c.training_shots_taken,1)
 def test_stadium_assignment_stable_home_and_training_no_rng(self):
  self.assertEqual(set(for_stadium(str(i)) for i in range(100)),set(STYLES))
  with isolated_game() as g:
   self.prepare(g);state=g.career.rng.getstate();g.shot_context='training';home_style=g.goal_net_style
   g.match_home=g.career.club;g.shot_context='match';self.assertEqual(g.goal_net_style,home_style)
   self.assertEqual(g.career.rng.getstate(),state)
 def test_box_swept_rear_roof_sides_and_no_phantom_veil(self):
  with isolated_game() as g:
   g._goal_net_style_override=NetStyle('box','square');g.draw=lambda:None
   b=g.ball;hw,h=g.goal_half_width,g.goal_height
   for old,end,velocity,axis,plane in (((0,-.2,1),(0,-8,1),(0,-80,0),1,-GOAL_DEPTH+b.radius),((0,-1,.3),(0,-1,5),(0,0,60),2,h-b.radius),((0,-1,1),(8,-1,1),(80,0,0),0,hw-b.radius),((0,-1,1),(-8,-1,1),(-80,0,0),0,-hw+b.radius)):
    b.x,b.y,b.z=end;b.vx,b.vy,b.vz=velocity;b.net_cooldown=0
    g._collide_net(*old)
    self.assertAlmostEqual((b.x,b.y,b.z)[axis],plane)
    self.assertLess((b.vx,b.vy,b.vz)[axis]*velocity[axis],0)
   b.x,b.y,b.z=0,-1,1;b.vx,b.vy,b.vz=0,-10,0
   g._collide_net(0,-.9,1);self.assertEqual(b.vy,-10)
 def test_box_ripple_seams_stay_closed(self):
  from career import NetRipple
  with isolated_game() as g:
   g._goal_net_style_override=NetStyle('box','hexagon')
   g.ripples=[NetRipple(s,.5,.5,.8) for s in ('back','left','right')]
   for ripple in g.ripples:ripple.age=.2
   h=g.goal_height
   for side,u in (('left',0.),('right',1.)):
    for v in (0.,.1,.35,.6,.9,1.):
     y,z=g._veil_profile(v)
     self.assertEqual(g._net_point('back',u,v),g._net_point(side,-y/GOAL_DEPTH,z/h))
 def test_all_nets_render_finite_and_within_mesh_limits(self):
  old=Window.size
  try:
   with isolated_game() as g:
    g.view='shot';g.shot_context='training'
    for style in STYLES:
     g._goal_net_style_override=style
     for size in ((1280,591),(640,360)):
      Window.size=size;g.size=size;g.draw();settle()
      for surface in ('back','left','right'):
       for u in (0,.3,.75,1):
        for v in (0,.5,1):self.assertTrue(all(math.isfinite(x) for x in g._net_point(surface,u,v)))
      for item in g.canvas.children:
       if isinstance(item,Mesh):self.assertLessEqual(len(item.indices),24000)
  finally:Window.size=old
