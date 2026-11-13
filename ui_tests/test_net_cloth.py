import copy,math,random,unittest
from unittest.mock import patch
from contextlib import ExitStack
from kivy.core.window import Window
from test_menus import isolated_game,settle
from goal_nets import STYLES,NetStyle
from net_cloth import NetCloth,NetGeometry
from net_render import NetRenderer
from net_presentation import ensure,impact,advance,ball_position
from goal_projection import project_point
from career import CAMERA_POSITION,CAMERA_FORWARD,CAMERA_UP,CAMERA_RIGHT,dot3,PHYSICS_STEP

class NetIntegration(unittest.TestCase):
 def test_projection_is_bit_identical_to_original_lateral_camera(self):
  with isolated_game() as g:
   for point in ((0,0,0),(-4,-2,1.3),(15,30,9),(-12,5,.115)):
    cx,cy,f=g.camera_values();relative=tuple(point[i]-CAMERA_POSITION[i] for i in range(3));depth=max(.05,dot3(relative,CAMERA_FORWARD))
    self.assertEqual(g.project(*point),(cx+f*dot3(relative,CAMERA_RIGHT)/depth,cy+f*dot3(relative,CAMERA_UP)/depth))
 def test_cloth_never_changes_physical_ball_or_goals_even_on_fast_scoring_shots(self):
  with patch('edition.WORLD_BUILD',True),isolated_game() as g:
   g.career.accept_starting_offer(g.career.offers[0]);g.career.attend_coach_meeting()
   g.draw=lambda:None;g.shot_context='training'
   for style in STYLES:
    g._goal_net_style_override=style
    for vx,vz in ((-4,0),(0,0),(4,0),(0,8),(0,-4)):
     states=[]
     for enabled in (False,True):
      g.reset_statistics();g.result_text='';g.outcome_registered=False;g.attempts=1;g.goals=0;g.goalkeeper_holding=False
      b=g.ball;b.reset(0,.1,1);b.vx=vx;b.vy=-30;b.vz=vz;b.active=True
      with ExitStack() as stack:
       stack.enter_context(patch.object(g,'_collide_goalkeeper',return_value=False));stack.enter_context(patch.object(g,'_collide_field_players'))
       if not enabled:stack.enter_context(patch('net_presentation.impact',return_value=False))
       for _ in range(240):g._update_ball(PHYSICS_STEP);advance(g,PHYSICS_STEP)
      states.append((copy.deepcopy(vars(b)),g.goals,g.result_text,g.last_goal_line_point))
     self.assertEqual(states[0],states[1])
 def test_net_keeps_recovering_between_shots_without_advancing_a_match(self):
  with isolated_game() as g:
   g.draw=lambda:None;g.view='hub';g._career_started=False;g.result_text='GOAL!'
   c=ensure(g);p=c.geometry.point('left',.24,.48)
   self.assertTrue(impact(g,'left',p,(-30,-10,0)))
   for _ in range(90):g.update(.1)
   self.assertFalse(c.active);self.assertEqual(c.displacement,0.)
 def test_idle_cache_reprojects_mutable_kivy_position_and_size(self):
  with isolated_game() as g:
   g.view='shot';g.draw();r=g._net_renderer;before=tuple(r.batches[0][2].vertices);count=r.rebuilds
   g.x+=80;g.draw()
   self.assertIs(r,g._net_renderer);self.assertGreater(r.rebuilds,count)
   self.assertAlmostEqual(r.batches[0][2].vertices[0]-before[0],80)
   count=r.rebuilds;g.width+=60;g.draw();self.assertGreater(r.rebuilds,count)
 def test_renderer_reuses_mesh_objects_and_sleeps_and_fits_mobile_batches(self):
  old=Window.size
  try:
   with isolated_game() as g:
    g.view='shot'
    for style in STYLES:
     g._goal_net_style_override=style
     for size in ((1280,591),(960,540),(640,360)):
      Window.size=size;g.size=size;g.draw();r=g._net_renderer;c=r.cloth;objects=[x[2] for x in r.batches]
      from kivy.graphics import Mesh
      render_ids={id(mesh) for row in r.batches for mesh in row[2:]}
      self.assertFalse(any(id(item) in render_ids for item in g.canvas.children))
      first=r.rebuilds;g.draw();self.assertEqual(first,r.rebuilds)
      for weights,indices,mesh,front in r.batches:
       self.assertLessEqual(len(indices),24000);self.assertTrue(all(math.isfinite(v) for v in mesh.vertices))
      g.result_text='GOAL!';b=g.ball;b.x,b.y,b.z=c.geometry.point('left',.25,.5);b.vx,b.vy,b.vz=-28,-12,0
      before=(copy.deepcopy(vars(b)),g.goals,g.attempts)
      self.assertTrue(impact(g,'left',(b.x,b.y,b.z),(-28,-12,0)))
      advance(g,.1);g.draw();self.assertEqual(objects,[x[2] for x in r.batches]);ball_position(g)
      self.assertEqual(before,(vars(b),g.goals,g.attempts))
      self.assertTrue(c.active);c.reset();g.result_text=''
  finally:Window.size=old
