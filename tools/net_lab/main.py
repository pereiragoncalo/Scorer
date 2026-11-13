"""Independent Scorer 1 net lab. Run from the repository; never opens a career."""
import argparse,json,math,sys
from dataclasses import asdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--preset',default='Near Post Strong');parser.add_argument('--structure',choices=('box','veil'),default='box')
parser.add_argument('--resolution',choices=('mobile','full'),default='mobile')
parser.add_argument('--mesh',choices=('square','hexagon'),default='square');parser.add_argument('--config',type=Path)
parser.add_argument('--capture',type=Path);parser.add_argument('--frames',type=int,default=240);parser.add_argument('--fps',type=int,default=60)
parser.add_argument('--playback',type=float,choices=(1.,.5,.25),default=1.);parser.add_argument('--view-only',action='store_true')
args,remaining=parser.parse_known_args();sys.argv=[sys.argv[0]]+remaining
from kivy.config import Config
Config.set('graphics','width','1280');Config.set('graphics','height','760')
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color,Rectangle,Line,Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from net_cloth import NetCloth,NetConfig
from net_render import NetRenderer
from goal_projection import project_point
from goal_nets import draw_box_frame,NetStyle
from career import CAMERA_VERTICAL_FOV
from tools.net_lab.scenarios import PRESETS,Replay

class Scene(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs);self.debug_mesh=False;self.renderer=None;self.mesh=args.mesh
        self.bind(pos=lambda *_:self.draw(),size=lambda *_:self.draw())
    def project(self,x,y,z):
        # Same camera position/axes; crop/zoom only for close inspection.
        focal=self.height/(2*math.tan(math.radians(CAMERA_VERTICAL_FOV)/2))*4.6
        origin=project_point(0,-1,1,0,0,focal)
        a,b=project_point(x,y,z,0,0,focal)
        return self.center_x+a-origin[0],self.center_y+b-origin[1]
    def pixels_per_meter(self,*_):return math.dist(self.project(0,0,0),self.project(1,0,0))
    @property
    def goal_half_width(self):return self.replay.geometry.width/2
    @property
    def goal_height(self):return self.replay.geometry.height
    def draw(self):
        if not hasattr(self,'replay'):return
        r=self.replay
        if self.renderer is None or self.renderer.cloth is not r.cloth or self.renderer.kind!=self.mesh:self.renderer=NetRenderer(r.cloth,self.mesh)
        self.canvas.clear()
        with self.canvas:
            Color(.025,.06,.08,1);Rectangle(pos=self.pos,size=self.size)
            Color(.035,.24,.12,1)
            from kivy.graphics import Mesh
            corners=[self.project(x,y,0) for x,y in ((-12,-8),(12,-8),(12,18),(-12,18))]
            Mesh(vertices=[n for x,y in corners for n in (x,y,0,0)],indices=[0,1,2,0,2,3],mode='triangles')
            Color(.5,.7,.5,.4);Line(points=[*self.project(-12,0,.01),*self.project(12,0,.01)],width=1)
        key=(tuple(self.pos),tuple(self.size))
        self.renderer.draw(self.canvas,self.project,key,r.ball if r.hit else None)
        with self.canvas:
            bx,by=self.project(*r.ball);scale=self.pixels_per_meter(*r.ball);radius=max(4,.115*scale)
            Color(.98,.98,.9,1);Ellipse(pos=(bx-radius,by-radius),size=(radius*2,radius*2))
            Color(.1,.13,.15,1);Line(circle=(bx,by,radius),width=1)
            Line(points=[bx-radius*.6,by,bx+radius*.6,by],width=.8)
        self.renderer.draw(self.canvas,self.project,key,r.ball if r.hit else None,foreground=True)
        with self.canvas:
            if r.geometry.structure=='box':draw_box_frame(self)
            else:
                hw,h=self.goal_half_width,self.goal_height
                Color(.96,.98,.98,1)
                Line(points=[*self.project(-hw,0,0),*self.project(-hw,0,h),*self.project(hw,0,h),*self.project(hw,0,0)],width=3)
                for x in (-hw,hw):Line(points=[*self.project(x,0,h),*self.project(x,-.55,h)],width=2)
        if self.debug_mesh:self.renderer.debug(self.canvas,self.project)

class Lab(App):
    def build(self):
        self.replay=Replay.load(args.config) if args.config else Replay(args.structure,preset=args.preset,coarse=args.resolution=='mobile')
        self.replay.playback=args.playback;self.a=None;self.b=None;self.frames=0
        root=BoxLayout(spacing=dp(8),padding=dp(8));self.scene=Scene();self.scene.replay=self.replay
        if not args.view_only:
            scroll=ScrollView(size_hint_x=None,width=dp(320));self.controls=BoxLayout(orientation='vertical',size_hint_y=None,spacing=dp(5));self.controls.bind(minimum_height=self.controls.setter('height'));scroll.add_widget(self.controls);root.add_widget(scroll)
            self.heading('SCORER 1 — NET LAB')
            self.preset=Spinner(text=self.replay.preset,values=tuple(PRESETS),size_hint_y=None,height=dp(44));self.preset.bind(text=self.choose_preset);self.controls.add_widget(self.preset)
            structure=Spinner(text=self.replay.geometry.structure,values=('box','veil'),size_hint_y=None,height=dp(44));structure.bind(text=self.structure);self.controls.add_widget(structure)
            mesh=Spinner(text=args.mesh,values=('square','hexagon'),size_hint_y=None,height=dp(44));mesh.bind(text=lambda _,v:setattr(self.scene,'mesh',v));self.controls.add_widget(mesh)
            resolution=Spinner(text='mobile' if self.replay.coarse else 'full',values=('mobile','full'),size_hint_y=None,height=dp(42));resolution.bind(text=lambda _,v:self.install(Replay(self.replay.geometry.structure,self.replay.cloth.config,self.replay.preset,v=='mobile')));self.controls.add_widget(resolution)
            self.buttons(('FIRE / REPEAT',lambda *_:self.fire()),('RESET NET',lambda *_:self.reset_net()))
            self.buttons(('PAUSE / PLAY',lambda *_:setattr(self.replay,'paused',not self.replay.paused)),('STEP 1/120',lambda *_:self.replay.one_step()))
            speed=Spinner(text=str(args.playback),values=('1.0','0.5','0.25'),size_hint_y=None,height=dp(42));speed.bind(text=lambda _,v:setattr(self.replay,'playback',float(v)));self.controls.add_widget(speed)
            self.buttons(('MESH DEBUG',lambda *_:setattr(self.scene,'debug_mesh',not self.scene.debug_mesh)),('SCREENSHOT',lambda *_:Window.screenshot(name='net-lab.png')))
            self.values={};self.sliders={}
            for key,lo,hi in (('force',3,50),('yaw',-65,65),('pitch',-40,40),('u',.03,.97),('v',.03,.97)):
                self.slider(key,lo,hi,getattr(self.replay,key),False)
            ranges=((0,.45),(8,80),(.8,12),(0,20),(.05,.9),(1.15,2.5),(5,120),(.0005,.015))
            for (key,value),(lo,hi) in zip(asdict(self.replay.cloth.config).items(),ranges):self.slider(key,lo,hi,value,True)
            self.buttons(('STORE A',lambda *_:self.store('a')),('STORE B',lambda *_:self.store('b')))
            self.buttons(('LOAD A',lambda *_:self.recall('a')),('LOAD B',lambda *_:self.recall('b')))
            self.path=TextInput(text=str(ROOT/'tools/net_lab/local-settings.json'),multiline=False,size_hint_y=None,height=dp(44));self.controls.add_widget(self.path)
            self.buttons(('SAVE JSON',lambda *_:self.save()),('LOAD JSON',lambda *_:self.load()))
        right=BoxLayout(orientation='vertical');right.add_widget(self.scene);self.info=Label(size_hint_y=None,height=dp(50),font_size=dp(15));right.add_widget(self.info);root.add_widget(right)
        if args.capture:args.capture.mkdir(parents=True,exist_ok=True)
        Clock.schedule_interval(self.update,1/args.fps);return root
    def heading(self,text):self.controls.add_widget(Label(text=text,size_hint_y=None,height=dp(24),font_size=dp(12)))
    def buttons(self,*items):
        row=BoxLayout(size_hint_y=None,height=dp(44),spacing=dp(4))
        for title,callback in items:
            button=Button(text=title,font_size=dp(12));button.bind(on_release=callback);row.add_widget(button)
        self.controls.add_widget(row)
    def slider(self,key,lo,hi,value,parameter):
        label=Label(text=f'{key}: {value:.3f}',font_size=dp(12),size_hint_y=None,height=dp(23));self.controls.add_widget(label)
        slider=Slider(min=lo,max=hi,value=value,size_hint_y=None,height=dp(32));self.controls.add_widget(slider)
        def change(_,v):
            label.text=f'{key}: {v:.3f}'
            if parameter:self.values[key]=v
            else:setattr(self.replay,key,v)
        slider.bind(value=change);self.sliders[key]=slider
        if parameter:self.values[key]=value
    def install(self,replay):
        speed=self.replay.playback;self.replay=replay;self.replay.playback=speed;self.scene.replay=replay
        if hasattr(self,'sliders'):
            for key,slider in self.sliders.items():slider.value=getattr(replay,key) if hasattr(replay,key) else getattr(replay.cloth.config,key)
    def choose_preset(self,_,value):self.install(Replay(self.replay.geometry.structure,self.replay.cloth.config,value,self.replay.coarse))
    def structure(self,_,value):self.install(Replay(value,self.replay.cloth.config,self.replay.preset,self.replay.coarse))
    def fire(self):
        self.replay.cloth=NetCloth(self.replay.geometry,NetConfig(**self.values),self.replay.coarse) if hasattr(self,'values') else self.replay.cloth
        self.replay.paused=False;self.replay.reset()
    def reset_net(self):self.replay.reset();self.replay.paused=True
    def snapshot(self):
        data=self.replay.configuration()
        if hasattr(self,'values'):data['parameters']=dict(self.values)
        return data
    def store(self,name):setattr(self,name,self.snapshot())
    def recall(self,name):
        value=getattr(self,name)
        if value:
            # Same validated JSON path as import, kept in a temporary dev file.
            import tempfile
            with tempfile.TemporaryDirectory() as tmp:
                p=Path(tmp)/'config.json';p.write_text(json.dumps(value));self.install(Replay.load(p))
    def save(self):
        try:Path(self.path.text).write_text(json.dumps(self.snapshot(),indent=2)+'\n');self.info.text='Configuration saved'
        except (OSError,ValueError) as e:self.info.text=str(e)
    def load(self):
        try:self.install(Replay.load(self.path.text))
        except (OSError,ValueError,KeyError,TypeError) as e:self.info.text=str(e)
    def update(self,dt):
        self.replay.advance(1/args.fps if args.capture else dt);self.scene.draw()
        r=self.replay;self.info.text=f'{r.preset} | t={r.tick/120:.2f}s | peak={r.peak:.3f}m at {r.peak_time:.2f}s | '+('moving' if r.cloth.active else 'rest')
        if args.capture:
            self.frames+=1
            # Capture after Kivy has drawn this tick, before advancing again.
            Clock.schedule_once(lambda _,n=self.frames:Window.screenshot(name=str(args.capture/f'frame-{n:04d}.png')),0)
            if self.frames>=args.frames:
                Clock.unschedule(self.update)
                (args.capture/'metrics.json').write_text(json.dumps({'config':r.configuration(),'frames':self.frames,'playback':r.playback,'peak_m':r.peak,'peak_time_s':r.peak_time},indent=2));Clock.schedule_once(lambda _:self.stop(),.05)

if __name__=='__main__':Lab().run()
