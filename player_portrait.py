"""Passport-style view of the existing player in a plain white T-shirt."""
from functools import lru_cache
from kivy.uix.image import Image
from kivy.graphics import Color,RoundedRectangle
from kivy.metrics import dp

@lru_cache(maxsize=1)
def passport_texture():
    from estate_portrait import outfit_texture
    # Reuse the approved casual frame: head, shoulders and upper T-shirt only.
    person=outfit_texture(1)
    crop=person.get_region(round(person.width*.16),round(person.height*.54),round(person.width*.68),round(person.height*.44))
    crop.mag_filter=crop.min_filter='nearest'
    return crop

class PlayerPortrait(Image):
    def __init__(self,**kwargs):
        super().__init__(texture=passport_texture(),fit_mode='contain',**kwargs)
        with self.canvas.before:
            Color(.70,.79,.81,1)
            self.frame=RoundedRectangle(radius=[dp(5)])
            Color(1,1,1,1)
        self.bind(pos=self._frame,size=self._frame,norm_image_size=self._frame)
        self._frame()
    def _frame(self,*_):
        w,h=self.norm_image_size
        self.frame.pos=(self.center_x-w/2,self.center_y-h/2)
        self.frame.size=(w,h)
