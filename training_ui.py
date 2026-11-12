"""One-screen training preparation with the existing player's locker-room portrait."""
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Color,RoundedRectangle,RenderContext
from kivy.metrics import dp,sp
from kivy.uix.progressbar import ProgressBar
from menu_ui import MenuTile,BoundedLabel,INK,MUTED,GREEN

KIT_SHADER='''$HEADER$
uniform vec3 shirt_colour;
uniform vec3 shorts_colour;
uniform vec3 socks_colour;
uniform float uv_bottom;
uniform float uv_top;
void main(void) {
 vec4 c=texture2D(texture0,tex_coord0);
 float y=(tex_coord0.y-uv_bottom)/(uv_top-uv_bottom);
 float lo=min(c.r,min(c.g,c.b));float hi=max(c.r,max(c.g,c.b));
 float light=(c.r+c.g+c.b)/3.0;
 if(hi-lo<0.13 && c.a>0.01) {
  if(y>0.48 && y<0.82 && light>0.28) c.rgb=(shirt_colour*0.90+vec3(0.035))*light*1.12;
  else if(y>0.30 && y<=0.48 && light>0.12) c.rgb=(shorts_colour*0.90+vec3(0.035))*clamp(light*2.8,0.15,1.0);
  else if(y>0.08 && y<0.25 && light>0.35) c.rgb=(socks_colour*0.90+vec3(0.035))*light*1.12;
 }
 gl_FragColor=c*frag_color;
}'''

class ClubTrainingPlayer(Image):
 def __init__(self,kit,**kwargs):
  self.canvas=RenderContext(use_parent_projection=True,use_parent_modelview=True)
  super().__init__(source='assets/training/seated_player.png',fit_mode='contain',**kwargs)
  self.canvas.shader.fs=KIT_SHADER
  self.canvas['uv_bottom']=0.0;self.canvas['uv_top']=1.0
  for key,colour in zip(('shirt_colour','shorts_colour','socks_colour'),kit[:3]):self.canvas[key]=tuple(colour[:3])
  self.bind(texture=self.sync_texture);self.sync_texture()
 def sync_texture(self,*_):
  t=self.texture
  if t:
   t.mag_filter=t.min_filter='nearest';self.canvas['uv_bottom']=float(t.tex_coords[1]);self.canvas['uv_top']=float(t.tex_coords[5])

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

class LockerPortrait(FloatLayout):
 def __init__(self,kit,**kwargs):
  super().__init__(**kwargs)
  self.room=Image(source='assets/training/locker_room.png',fit_mode='contain');self.add_widget(self.room)
  self.player=ClubTrainingPlayer(kit,size_hint=(None,None));self.add_widget(self.player)
  self.bind(pos=self.fit,size=self.fit);self.room.bind(norm_image_size=self.fit);self.fit()
 def fit(self,*_):
  self.room.pos=self.pos;self.room.size=self.size
  rw,rh=self.room.norm_image_size
  if not rw or not rh:return
  ph=rh*.70;pw=ph*self.player.texture.width/self.player.texture.height if self.player.texture else ph*.6
  self.player.size=(pw,ph);self.player.pos=(self.center_x-pw/2,self.center_y-rh/2+rh*.005)

class TrainingScreen(BoxLayout):
 def __init__(self,menu):
  super().__init__(orientation='vertical',padding=dp(12),spacing=dp(8));self.menu=menu;g=menu.game;c=g.career;self.loc=g.i18n
  from player_development import NAMES,needed
  self.header=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(8));self.add_widget(self.header)
  self.title=self.label('TRAINING',20,GREEN);self.title.size_hint_y=1;self.header.add_widget(self.title)
  self.help=MenuTile('HELP',lambda:menu.action('help'),size_hint=(None,None));self.help.width=dp(64);self.help.height=dp(48);self.header.add_widget(self.help)
  self.back=MenuTile('BACK',lambda:menu.action('hub'),size_hint=(None,None));self.back.width=dp(76);self.back.height=dp(48);self.header.add_widget(self.back)
  body=BoxLayout(spacing=dp(12));self.add_widget(body)
  left=BoxLayout(orientation='vertical',size_hint_x=.55,spacing=dp(4));body.add_widget(left)
  portrait=LockerPortrait(c.kit_for_club(c.club) if c.club else ((.2,.4,.7,1),)*3);left.add_widget(portrait);self.room=portrait.room;self.player=portrait.player
  self.name=self.label(c.player_name,16,INK,False);self.name.height=dp(32);left.add_widget(self.name)
  self.controls=BoxLayout(orientation='vertical',size_hint_x=.45,spacing=dp(8));body.add_widget(self.controls)
  self.focus=self.label(NAMES[c.training_focus],18,GREEN);self.controls.add_widget(self.focus)
  used=c.trained_this_week;resumable=c.training_session_week==c.week and not used
  shots=c.training_shots_taken if c.training_session_week==c.week or used else 0;goals=c.training_session_goals if c.training_session_week==c.week or used else 0
  self.progress=self.label(g.i18n.tr('Completed shots: {shots}/3 · Goals: {goals}/3',shots=shots,goals=goals),13,INK,False);self.controls.add_widget(self.progress)
  self.shots_bar=ProgressBar(max=3,value=shots,size_hint_y=None,height=dp(10));self.controls.add_widget(self.shots_bar)
  skill=c.development['skills'][c.training_focus];level=skill['level']
  self.skill=self.label('MAXIMUM LEVEL' if level==10 else g.i18n.tr('Level {level}/10 · XP {xp}/{needed}',level=level,xp=skill['xp'],needed=needed(level)),13,INK,False);self.controls.add_widget(self.skill)
  self.energy=self.label(g.i18n.tr('Energy: {energy}/20  ·  Morale: {morale}/20',energy=f'{c.stamina:.1f}',morale=f'{c.morale:.1f}'),13,MUTED,False);self.controls.add_widget(self.energy)
  self.controls.add_widget(Widget())
  self.error_label=None
  if c.message.startswith(('Unable ','Could not ')):
   self.error_label=self.label(c.message,12,INK);self.error_label.height=dp(32);self.controls.add_widget(self.error_label)
  self.start=MenuTile('TRAINING COMPLETE' if used else 'RESUME TRAINING' if resumable else 'START TRAINING',lambda:menu.action('training_start'),accent=True);self.start.height=dp(48)
  self.start.disabled=used or c.coach_meeting_required;self.controls.add_widget(self.start)
  with self.canvas.before:Color(.025,.075,.085,.98);self.panel=RoundedRectangle(pos=self.pos,size=self.size,radius=[dp(12)])
  self.bind(pos=self.fit,size=self.fit);self.controls.bind(height=self.fit);self.fit()
 def label(self,text,size,colour,localize=True):
  return BoundedLabel(text=text,localize=localize,font_size=sp(size),color=colour,halign='left',size_hint_y=None,height=dp(40))
 def fit(self,*_):
  self.panel.pos=self.pos;self.panel.size=self.size
  remaining=max(1,self.controls.height-dp(48)-self.controls.spacing*(len(self.controls.children)-1)-dp(10)-(self.error_label.height if self.error_label else 0));factor=min(1,remaining/dp(156))
  for w,h in ((self.focus,40),(self.progress,40),(self.skill,32),(self.energy,44)):w.height=dp(h)*factor
