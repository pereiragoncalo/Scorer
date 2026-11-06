"""Original props and crowd atlases: nearest sampling, cached palette recolouring."""
from collections import OrderedDict
from pathlib import Path
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
from kivy.graphics import Color,Rectangle
ROOT=Path(__file__).resolve().parent
class SceneTextures:
    def __init__(self,limit=8):self.sources={};self.entries=OrderedDict();self.payloads={};self.limit=limit;self.allocations=0
    def _reload(self,texture):
        data=self.payloads.get(id(texture))
        if data:texture.blit_buffer(data,colorfmt='rgba',bufferfmt='ubyte')
        texture.mag_filter=texture.min_filter='nearest'
    def get(self,name,palette=None):
        key=(name,tuple(tuple(c) for c in palette) if palette else None)
        if key in self.entries:self.entries.move_to_end(key);return self.entries[key]
        if name not in self.sources:
            t=CoreImage(str(ROOT/'assets/sprites/scene'/name)).texture
            self.sources[name]=(t.size,bytes(t.pixels),t.tex_coords)
        size,source,coords=self.sources[name];pixels=bytearray(source)
        if palette:
            mapping={a:bytes(round(max(0,min(1,x))*255) for x in b[:3]) for a,b in zip(((40,80,210),(240,240,220)),palette)}
            for i in range(0,len(pixels),4):
                value=mapping.get(tuple(pixels[i:i+3]))
                if pixels[i+3] and value:pixels[i:i+3]=value
        texture=Texture.create(size=size,colorfmt='rgba');payload=bytes(pixels);texture.blit_buffer(payload,colorfmt='rgba',bufferfmt='ubyte')
        if coords[1]>coords[5]:texture.flip_vertical()
        self.payloads[id(texture)]=payload;texture.add_reload_observer(self._reload);texture.mag_filter=texture.min_filter='nearest'
        self.entries[key]=texture;self.allocations+=1
        if len(self.entries)>self.limit:
            _,old=self.entries.popitem(last=False);old.remove_reload_observer(self._reload);self.payloads.pop(id(old),None)
        return texture

def cache(game):
    if not hasattr(game,'_scene_textures'):game._scene_textures=SceneTextures()
    return game._scene_textures

def uv(texture,column,row,columns,rows):
    u0,u1=column/columns,(column+1)/columns;bottom,top=texture.tex_coords[1],texture.tex_coords[5]
    vb=top+(bottom-top)*(row+1)/rows;vt=top+(bottom-top)*row/rows
    return (u0,vb,u1,vb,u1,vt,u0,vt)

def ball(game,x,y,radius):
    texture=cache(game).get('ball.png')
    # Visual spin only; never use elapsed time to advance the ball's physics.
    speed=abs(getattr(game.ball,'vx',0))+abs(getattr(game.ball,'vy',0))+abs(getattr(game.ball,'vz',0))
    frame=int(game.elapsed*min(18.,speed*.8))%8 if game.ball.active else 0
    Color(1,1,1,1);Rectangle(texture=texture,tex_coords=uv(texture,frame,0,8,1),pos=(x-radius,y-radius),size=(radius*2,radius*2))
