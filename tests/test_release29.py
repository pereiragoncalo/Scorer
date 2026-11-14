import math,unittest
from bisect import bisect_right
from goal_nets import STYLES
from net_cloth import NetGeometry
from net_drape import ReferenceCloth,MATERIALS,RollingReplay
from net_strands import panel_strands,joining_seams
from net_contact import ClothContacts

class ClosedRoundedSeams(unittest.TestCase):
 def test_fibres_fill_the_strip_between_analytic_curve_and_physical_boundary(self):
  for coarse in (True,False):
   c=ReferenceCloth(NetGeometry('rounded',depth=3.5),MATERIALS['rounded'].config,coarse)
   g=c.geometry;path=tuple(c.grids['left'][0]);z=[g.profile(u)[1]for u in path]
   for side in ('left','right'):
    edges=panel_strands(g,side,'hexagon',.28,path)
    boundary=[u for edge in edges for u,v in edge if v>.99999]
    self.assertGreater(len(boundary),10)
    filled=[]
    for u in boundary:
     i=max(0,min(len(path)-2,bisect_right(path,u)-1));t=(u-path[i])/(path[i+1]-path[i])
     filled.append(z[i]+(z[i+1]-z[i])*t-g.profile(u)[1])
    self.assertGreater(max(filled),.001)
    self.assertTrue(all(0<=q<=1 for edge in edges for uv in edge for q in uv))
 def test_both_seams_are_shared_in_collision_triangles_and_rendered_without_gaps(self):
  for coarse in (True,False):
   c=ReferenceCloth(NetGeometry('rounded',depth=3.5),MATERIALS['rounded'].config,coarse)
   mesh=ClothContacts(c);path=c.grids['back'][1];back=c.grids['back'][2]
   seams=joining_seams(c)
   for side,edge,u in (('left',0,0.),('right',-1,1.)):
    self.assertEqual([pair for pair in seams if pair[0][0]==u],[((u,a),(u,b))for a,b in zip(path,path[1:])])
    for j in range(len(path)-1):
     pair={back[j][edge],back[j+1][edge]}
     if all(c.rest[i][2]<1e-7 for i in pair):continue
     for panel in ('back',side):self.assertTrue(any(pair<=set(tri)for tri in mesh.triangles[panel]))
 def test_drawn_join_remains_continuous_under_impacts_from_both_sides(self):
  for sign,side,edge in ((-1,'left',0),(1,'right',1)):
   r=RollingReplay('rounded',height=1.,geometry=NetGeometry('rounded',depth=3.5),coarse=True)
   r.position=[sign*2.8,-.02,1.];r.velocity=[sign*4.,-25.,0.];r.ball=tuple(r.position)
   for _ in range(90):r.one_step()
   self.assertGreater(r.peak,.1)
   for i in range(101):self.assertLess(math.dist(r.cloth.sample('back',edge,i/100),r.cloth.sample(side,i/100,1)),1e-6)
