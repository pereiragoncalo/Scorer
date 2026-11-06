#!/usr/bin/env python3
"""Approval-only Scorer sprite viewer. Run from any working directory."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kivy.config import Config
Config.set('graphics','width','1440')
Config.set('graphics','height','900')
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from tools.sprite_lab.animation import Animation,load_manifest
from tools.sprite_lab.textures import TextureCache,DEFAULT_PLAYER,DEFAULT_KEEPER,rgb

def button(text,callback):
    b=Button(text=text,font_size=14,background_normal='',background_color=(.12,.25,.30,1))
    b.bind(on_release=lambda _:callback())
    return b

class Stage(BoxLayout):
    def __init__(self,panel,**kwargs):
        super().__init__(**kwargs);self.panel=panel
        self.bind(pos=lambda *_:self.redraw(),size=lambda *_:self.redraw())

    def draw_image(self,texture,coords,x,y,w,h,flip=False):
        if flip:
            coords=(coords[2],coords[3],coords[0],coords[1],coords[6],coords[7],coords[4],coords[5])
        Color(1,1,1,1);Rectangle(texture=texture,tex_coords=coords,pos=(round(x),round(y)),size=(w,h))

    def redraw(self):
        p=self.panel;a=p.animation;c=a.character;cache=p.lab.cache;clip=a.clip
        key=(tuple(self.pos),tuple(self.size),a.state,a.frame,a.paused,a.speed,a.flipped,p.view,p.mode,p.colours,p.lab.scale,p.lab.anchors)
        if getattr(self,'_last_draw',None)==key:return
        self._last_draw=key
        self.canvas.clear()
        with self.canvas:
            Color(.055,.26,.16,1);Rectangle(pos=self.pos,size=self.size)
            Color(.10,.33,.20,1);Rectangle(pos=(self.x,self.y+self.height*.5),size=(self.width,self.height*.5))
            Color(.35,.58,.38,1);Line(points=[self.x,self.y+25,self.right,self.y+25],width=1)
            w,h=c['canvas'];scale=p.lab.scale
            if p.mode=='Animation':
                scale=max(1,min(scale,int((self.width-16)/w),int((self.height-32)/h)))
                texture,coords=cache.frame(c,clip,p.view,a.frame,p.colours)
                ax,ay=c['anchor'];x=self.center_x-ax*scale;y=self.y+26-(h-ay)*scale
                self.draw_image(texture,coords,x,y,w*scale,h*scale,a.flipped)
                if p.lab.anchors:
                    Color(1,.75,.2,1);Line(rectangle=(x,y,w*scale,h*scale),width=1)
                    Line(points=[self.center_x-7,self.y+26,self.center_x+7,self.y+26],width=1)
                    Line(points=[self.center_x,self.y+19,self.center_x,self.y+33],width=1)
            elif p.mode=='Sheet':
                t=cache.get(clip['sheets'][p.view]['path'],p.colours)
                s=max(1,min(scale,int((self.width-8)/t.width),int((self.height-8)/t.height)))
                self.draw_image(t,t.tex_coords,self.center_x-t.width*s/2,self.center_y-t.height*s/2,t.width*s,t.height*s,a.flipped)
            else:
                cols=min(4,clip['frames']);rows=(clip['frames']+cols-1)//cols
                s=max(1,min(scale,int((self.width-8)/(cols*w)),int((self.height-8)/(rows*h))))
                left=self.center_x-cols*w*s/2;top=self.center_y+rows*h*s/2
                for i,path in enumerate(clip['individuals'][p.view]):
                    t=cache.get(path,p.colours)
                    self.draw_image(t,t.tex_coords,left+(i%cols)*w*s,top-(i//cols+1)*h*s,w*s,h*s,a.flipped)
        p.status.text=f'{a.state}   FRAME {a.frame+1:02}/{clip["frames"]:02}   {clip["fps"]*a.speed:.1f} fps   {"PAUSED" if a.paused else "PLAYING"}'

class CharacterPanel(BoxLayout):
    def __init__(self,lab,role,**kwargs):
        super().__init__(orientation='vertical',spacing=5,padding=6,**kwargs)
        self.lab=lab;self.role=role;c=lab.manifest['characters'][role]
        self.animation=Animation(c,next(iter(c['animations'])))
        self.view=c['views'][0];self.mode='Animation'
        self.colours=DEFAULT_PLAYER if role=='players' else DEFAULT_KEEPER
        self.add_widget(Label(text='FIELD PLAYER' if role=='players' else 'GOALKEEPER',size_hint_y=None,height=28,bold=True))
        grid=GridLayout(cols=4,size_hint_y=None,height=93,spacing=4)
        for state in c['animations']:
            grid.add_widget(button(state.replace('_',' '),lambda state=state:self.select(state)))
        self.add_widget(grid)
        row=BoxLayout(size_hint_y=None,height=36,spacing=4)
        row.add_widget(button('Mirror',self.flip))
        view=Spinner(text=self.view,values=c['views'],font_size=14);view.bind(text=self.change_view);row.add_widget(view)
        mode=Spinner(text=self.mode,values=('Animation','Frames','Sheet'),font_size=14);mode.bind(text=self.change_mode);row.add_widget(mode)
        self.add_widget(row)
        self.status=Label(size_hint_y=None,height=28,font_size=13)
        self.add_widget(self.status)
        self.stage=Stage(self);self.add_widget(self.stage)
        self.add_widget(Label(text='SHIRT / SECONDARY / SHORTS / SOCKS / GLOVES  (hex)',font_size=12,size_hint_y=None,height=22))
        palette=BoxLayout(size_hint_y=None,height=34,spacing=3);self.fields=[]
        for value in self.colours:
            field=TextInput(text=value,multiline=False,font_size=13,padding=[4,7]);self.fields.append(field);palette.add_widget(field)
        palette.add_widget(button('Apply',self.apply));self.add_widget(palette)
        presets=BoxLayout(size_hint_y=None,height=32,spacing=3)
        for name,values in [('Vitória',('FF0000','000000','000000','FF0000','FFFFFF')),('Blue/white',('3EA0FF','FFFFFF','FFFFFF','FFFFFF','FFFFFF')),('Keeper',DEFAULT_KEEPER)]:
            presets.add_widget(button(name,lambda values=values:self.preset(values)))
        self.add_widget(presets)

    def select(self,state): self.animation.select(state);self.stage.redraw()
    def flip(self): self.animation.flipped=not self.animation.flipped;self.stage.redraw()
    def change_view(self,_,value): self.view=value;self.stage.redraw()
    def change_mode(self,_,value): self.mode=value;self.stage.redraw()
    def apply(self):
        try:
            values=tuple(f.text.strip().lstrip('#').upper() for f in self.fields)
            for value in values: rgb(value)
            self.colours=values;self.lab.message.text='Palette applied; original game kits unchanged.';self.stage.redraw()
        except ValueError:
            self.lab.message.text='Invalid colour: use six hexadecimal digits, e.g. FF0000.'
    def preset(self,values):
        for field,value in zip(self.fields,values):field.text=value
        self.apply()

class SpriteLab(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(orientation='vertical',padding=8,spacing=6,**kwargs)
        self.manifest=load_manifest();self.cache=TextureCache(self.manifest,limit=32)
        self.scale=5;self.anchors=True;self.panels=[]
        self.add_widget(Label(text='SCORER  /  ORIGINAL 8-BIT SPRITE LAB  /  VISUAL APPROVAL PREVIEW',size_hint_y=None,height=30,bold=True))
        controls=BoxLayout(size_hint_y=None,height=40,spacing=5)
        controls.add_widget(button('Pause / play',self.pause));controls.add_widget(button('< Frame',lambda:self.step(-1)));controls.add_widget(button('Frame >',lambda:self.step(1)))
        controls.add_widget(button('Anchors',self.toggle_anchors));controls.add_widget(button('Repeat / hold',self.toggle_repeat))
        self.add_widget(controls)
        row=BoxLayout(size_hint_y=None,height=36,spacing=4)
        self.speed_label=Label(text='Speed 1.00x',size_hint_x=.25);row.add_widget(self.speed_label)
        speed=Slider(min=.25,max=2,step=.05,value=1);speed.bind(value=self.speed);row.add_widget(speed)
        row.add_widget(Label(text='Pixel scale',size_hint_x=.25));scale=Spinner(text='5',values=tuple(str(i) for i in range(1,9)),size_hint_x=.2);scale.bind(text=self.change_scale);row.add_widget(scale)
        self.add_widget(row)
        columns=BoxLayout(spacing=8)
        for role in ('players','goalkeeper'):
            panel=CharacterPanel(self,role);self.panels.append(panel);columns.add_widget(panel)
        self.add_widget(columns)
        self.message=Label(text='Separate viewer. No game physics, collisions or saved careers are loaded.',font_size=13,size_hint_y=None,height=26)
        self.add_widget(self.message)
        self.tick_event=Clock.schedule_interval(self.tick,1/60)
    def tick(self,dt):
        for p in self.panels:p.animation.update(dt);p.stage.redraw()
    def pause(self):
        value=not all(p.animation.paused for p in self.panels)
        for p in self.panels:p.animation.paused=value
    def step(self,delta):
        for p in self.panels:p.animation.step(delta);p.stage.redraw()
    def toggle_anchors(self): self.anchors=not self.anchors
    def toggle_repeat(self):
        for p in self.panels:p.animation.repeat=not p.animation.repeat
        self.message.text='Repeat: '+str(self.panels[0].animation.repeat)+' (hold respects the one-shot clip endings).'
    def speed(self,_,value):
        self.speed_label.text=f'Speed {value:.2f}x'
        for p in self.panels:p.animation.speed=value
    def change_scale(self,_,value):self.scale=int(value)

class SpriteViewerApp(App):
    title='Scorer — Sprite Approval Lab'
    def build(self):return SpriteLab()

if __name__=='__main__':SpriteViewerApp().run()
