"""Kivy text adapters: translate UI text, keep editable text and names opaque."""
from functools import wraps
from localization import current, using
from kivy.uix.textinput import TextInput


def localized_call(func):
    @wraps(func)
    def call(self,*args,**kwargs):
        localizer=getattr(self,'i18n',None) or getattr(self,'_localizer',None) or getattr(getattr(self,'game',None),'i18n',None)
        if localizer is None and args:localizer=getattr(args[0],'i18n',None)
        with using(localizer or current()):return func(self,*args,**kwargs)
    return call


class LocalizedText:
    def __init__(self,**kwargs):
        self._i18n=kwargs.pop('localizer',None) or current()
        self._translate=kwargs.pop('localize',True)
        self._explicit_font=kwargs.get('font_name')
        raw=kwargs.get('text','')
        kwargs['text']=self._i18n.tr(raw) if self._translate else raw
        kwargs['font_name']=self._i18n.font(kwargs['text'],self._explicit_font)
        super().__init__(**kwargs)
        self._rendered_text=self.text;self._translating=False
        self.bind(text=self._localized_text)

    def _localized_text(self,*_):
        if self._translating or self.text==self._rendered_text:return
        self._translating=True
        try:
            if self._translate:self.text=self._i18n.tr(self.text)
            self.font_name=self._i18n.font(self.text,self._explicit_font)
            self._rendered_text=self.text
        finally:self._translating=False


class LocalizedInput(TextInput):
    def __init__(self,**kwargs):
        self._i18n=current()
        kwargs['hint_text']=self._i18n.tr(kwargs.get('hint_text',''))
        kwargs.setdefault('font_name',self._i18n.font(kwargs.get('text','')+kwargs['hint_text']))
        super().__init__(**kwargs)
        self.bind(text=self._input_font)

    def _input_font(self,*_):
        self.font_name=self._i18n.font(self.text+self.hint_text)

from kivy.uix.popup import Popup

class LocalizedPopup(Popup):
    def __init__(self,**kwargs):
        localizer=current();kwargs['title']=localizer.tr(kwargs.get('title',''))
        kwargs['title_font']=localizer.font(kwargs['title'])
        super().__init__(**kwargs)
