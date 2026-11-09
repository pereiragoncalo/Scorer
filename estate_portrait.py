"""A live illustrated portrait of the best owned home, clothes and parked car."""
from functools import lru_cache
from kivy.uix.widget import Widget
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color,Rectangle,StencilPush,StencilUse,StencilUnUse,StencilPop
from career_life import best_assets
OUTFITS={None:0,'casual':1,'smart':2,'suit':3,'designer':4}
@lru_cache(maxsize=24)
def core_image(path):
    return CoreImage(path)
def texture(path):
    image=core_image(path);image.texture.mag_filter=image.texture.min_filter='nearest'
    return image.texture
@lru_cache(maxsize=5)
def outfit_texture(index):
    sheet=texture('assets/lifestyle/scene/outfits.png');left=round(sheet.width*index/5);right=round(sheet.width*(index+1)/5)
    region=sheet.get_region(left,0,right-left,sheet.height);region.mag_filter=region.min_filter='nearest';return region
@lru_cache(maxsize=1)
def background_texture():
    image=texture('assets/lifestyle/scene/forecourt.png');height=min(image.height,round(image.width/2.4))
    region=image.get_region(0,(image.height-height)//2,image.width,height);region.mag_filter=region.min_filter='nearest';return region
class EstatePortrait(Widget):
    def __init__(self,career,**kwargs):
        super().__init__(**kwargs);self.selection=best_assets(career)
        self.scene_items={kind:row[0] if row else None for kind,row in self.selection.items()}
        self.house=texture('assets/lifestyle/'+(self.scene_items['home'] or 'studio')+'.png')
        self.car=texture('assets/lifestyle/'+self.scene_items['car']+'.png') if self.scene_items['car'] else None
        self.person=outfit_texture(OUTFITS[self.scene_items['clothes']]);self.background=background_texture()
        self.bind(pos=self.render,size=self.render);self.render()
    def render(self,*_):
        width=min(self.width,self.height*2.4);height=width/2.4;x=self.center_x-width/2;y=self.center_y-height/2
        self.photo_rect=(x,y,width,height);self.canvas.clear()
        with self.canvas:
            Color(1,1,1,1);StencilPush();Rectangle(pos=(x,y),size=(width,height));StencilUse()
            Rectangle(texture=self.background,pos=(x,y),size=(width,height))
            house_height=height*.96;house_width=house_height*self.house.width/self.house.height
            hx=x+width*.035;hy=y+height*.08
            Rectangle(texture=self.house,pos=(hx,hy),size=(house_width,house_height))
            if self.car:
                cw=width*.39;ch=cw*self.car.height/self.car.width
                Rectangle(texture=self.car,pos=(x+width*.56,y+height*.04),size=(cw,ch))
            ph=height*.46;pw=ph*self.person.width/self.person.height
            px=hx+house_width*.49-pw/2
            Rectangle(texture=self.person,pos=(px,y+height*.075),size=(pw,ph))
            StencilUnUse();Rectangle(pos=(x,y),size=(width,height));StencilPop()
