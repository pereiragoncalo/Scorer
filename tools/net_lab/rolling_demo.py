"""Capture only the rolling-contact development comparison. No game build/run."""
import argparse,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--capture',type=Path,required=True);p.add_argument('--frames',type=int,default=300);p.add_argument('--playback',type=float,default=1.);p.add_argument('--matrix',choices=['square','hexagon']);options=p.parse_args();sys.argv=[sys.argv[0]]
from kivy.config import Config
Config.set('graphics','width','1280');Config.set('graphics','height','1080' if options.matrix else '720')
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stencilview import StencilView
from kivy.graphics import Canvas,Color,Rectangle,Line,Ellipse
from net_render import NetRenderer
from goal_projection import project_point
from career import CAMERA_VERTICAL_FOV
from retro_props import uv
from tools.net_lab.rolling_contact import RollingReplay

class View(StencilView):
 def __init__(self,replay,**kwargs):
  super().__init__(**kwargs);self.replay=replay;self.paint=Canvas();self.canvas.add(self.paint);self.renderer=NetRenderer(replay.cloth,options.matrix or 'square')
  self.texture=CoreImage(str(ROOT/'assets/sprites/scene/ball.png')).texture;self.texture.mag_filter=self.texture.min_filter='nearest'
 def project(self,x,y,z):
  focal=self.height/(2*math.tan(math.radians(CAMERA_VERTICAL_FOV)/2))*4.7
  ox,oy=project_point(-3.1,-1.45,.95,0,0,focal);px,py=project_point(x,y,z,0,0,focal)
  return self.center_x+px-ox,self.center_y+py-oy
 def draw(self):
  r=self.replay;g=r.geometry;self.paint.clear()
  with self.paint:
   Color(.025,.055,.065,1);Rectangle(pos=self.pos,size=self.size)
   Color(.035,.26,.13,1);Rectangle(pos=self.pos,size=(self.width,self.height*.54))
   Color(.42,.62,.42,.4);Line(points=[*self.project(-6,0,.005),*self.project(2,0,.005)],width=1)
  key=(tuple(self.pos),tuple(self.size));self.renderer.draw(self.paint,self.project,key,r.ball if r.hit else None)
  with self.paint:
   x,y=self.project(*r.ball);sx,sy=self.project(r.ball[0],r.ball[1],.005)
   scale=math.dist(self.project(r.ball[0],r.ball[1],0),self.project(r.ball[0],r.ball[1],1));radius=max(5,r.radius*scale)
   Color(0,0,0,.35);Ellipse(pos=(sx-radius*.95,sy-radius*.22),size=(radius*1.9,radius*.44))
   Color(1,1,1,1);frame=int(r.roll/(2*math.pi)*8)%8
   Rectangle(texture=self.texture,tex_coords=uv(self.texture,frame,0,8,1),pos=(x-radius,y-radius),size=(radius*2,radius*2))
  self.renderer.draw(self.paint,self.project,key,r.ball if r.hit else None,foreground=True)
  with self.paint:
   hw,h=g.width/2,g.height
   Color(.95,.97,.98,1);Line(points=[*self.project(-hw,0,0),*self.project(-hw,0,h),*self.project(hw,0,h),*self.project(hw,0,0)],width=3)
   for x in (-hw-.35,0,hw+.35):
    Color(.38,.45,.46,1);Line(points=[*self.project(x,-g.depth-1,0),*self.project(x,-g.depth-1,h+.65)],width=2)
    Color(.8,.85,.81,.8);Line(points=[*self.project(x,-g.depth-1,h+.6),*self.project(max(-hw,min(hw,x)),-g.depth,h)],width=.7)

class Demo(App):
 def build(self):
  self.replays=([RollingReplay('sagged',speed,height) for height in (.22,1.1,2.05) for speed in (4.,9.,18.)] if options.matrix else [RollingReplay('tight'),RollingReplay('slack')]);self.views=[];self.frame=0;self.acc=0.
  root=BoxLayout(orientation='vertical',padding=8,spacing=6)
  root.add_widget(Label(text=('MALHA '+('HEXAGONAL' if options.matrix=='hexagon' else 'QUADRADA')+' · MAIS FOLGA · BASE FIXA NA RELVA' if options.matrix else 'BASE FIXA NA RELVA · FOLGA APENAS NA MALHA SUSPENSA'),size_hint_y=None,height=32,font_size=17))
  panels=GridLayout(cols=3,spacing=8) if options.matrix else BoxLayout(spacing=10)
  for index,r in enumerate(self.replays):
   column=BoxLayout(orientation='vertical');column.add_widget(Label(text=((('BAIXA','MÉDIA','ALTA')[index//3]+' · '+('LENTA 4 m/s','MÉDIA 9 m/s','RÁPIDA 18 m/s')[index%3]) if options.matrix else r.material.label),size_hint_y=None,height=36,font_size=17 if options.matrix else 22))
   view=View(r);self.views.append(view);column.add_widget(view);panels.add_widget(column)
  root.add_widget(panels)
  self.info=Label(size_hint_y=None,height=30,font_size=15);root.add_widget(self.info)
  options.capture.mkdir(parents=True,exist_ok=True);Clock.schedule_interval(self.update,1/60)
  return root
 def update(self,_dt):
  self.acc+=options.playback/60
  while self.acc+1e-12>=RollingReplay.STEP:
   for r in self.replays:r.one_step()
   self.acc-=RollingReplay.STEP
  for v in self.views:v.draw()
  self.info.text=f'{self.replays[0].tick*RollingReplay.STEP:.2f} s'+('  ·  CÂMARA LENTA 50%' if options.playback==.5 else '')
  self.frame+=1
  Clock.schedule_once(lambda _,n=self.frame:Window.screenshot(name=str(options.capture/f'frame-{n:04d}.png')),0)
  if self.frame>=options.frames:
   Clock.unschedule(self.update)
   data=[]
   for r in self.replays:data.append({'material':r.material.label,'final_position':r.ball,'peak_deformation':r.peak,'stop_time':r.stop_time,'history':r.history})
   (options.capture/'metrics.json').write_text(json.dumps(data,indent=2));Clock.schedule_once(lambda _:self.stop(),.05)

if __name__=='__main__':Demo().run()
