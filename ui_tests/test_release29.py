import copy,math,unittest
from test_menus import isolated_game
from goal_nets import STYLES,ROUNDED_STYLE
from net_presentation import ensure
from net_render import NetRenderer
from net_strands import joining_seams

class RenderedClosedSeams(unittest.TestCase):
 def test_both_seams_are_complete_in_actual_gles_line_batches(self):
  with isolated_game()as g:
   g._goal_net_style_override=ROUNDED_STYLE;c=ensure(g)
   for low in (True,False):
    before=copy.deepcopy(c.positions);r=NetRenderer(c,'hexagon',low)
    r.sync(g.project,(g.pos,g.size,g.desktop_windows));self.assertEqual(c.positions,before)
    world=r._world[0];edges=r.batches[0][1]
    actual=[(world[edges[i]],world[edges[i+1]])for i in range(0,len(edges),2)]
    for a,b in joining_seams(c):
     p,q=c.sample('back',*a),c.sample('back',*b)
     self.assertTrue(any(math.dist(p,x)<1e-5 and math.dist(q,y)<1e-5 or math.dist(q,x)<1e-5 and math.dist(p,y)<1e-5 for x,y in actual))
 def test_all_nine_styles_fit_mobile_budget_and_renderer_has_no_physics_side_effects(self):
  with isolated_game()as g:
   for style in STYLES:
    g._goal_net_style_override=style;c=ensure(g);before=copy.deepcopy(c.positions);ball=vars(g.ball).copy()
    for low in (True,False):
     r=NetRenderer(c,style.mesh,low);r.sync(g.project,(g.pos,g.size,g.desktop_windows))
     for weights,edges,_,_ in r.batches:self.assertLessEqual(len(edges),24000);self.assertLess(len(weights),16000)
    self.assertEqual(c.positions,before);self.assertEqual(vars(g.ball),ball)

 def test_contact_overlay_still_draws_over_the_ball_on_the_near_side(self):
  with isolated_game()as g:
   g._goal_net_style_override=ROUNDED_STYLE;c=ensure(g)
   point=c.sample('left',.3,.5)
   self.assertTrue(c.impact('left',point,(-30.,-10.,0.)))
   r=NetRenderer(c,'hexagon',True);before=copy.deepcopy(c.positions)
   r.sync(g.project,(g.pos,g.size,g.desktop_windows),point)
   self.assertTrue(any(len(front.indices)>0 for _,_,_,front in r.batches))
   self.assertEqual(c.positions,before)
