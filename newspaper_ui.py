"""A measured, single-page sports newspaper. No scrolling, cropping or ellipses."""
from functools import lru_cache
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color,Rectangle
from kivy.metrics import dp,sp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from menu_ui import MenuTile
from newspaper import article,current_report,brief_article

INK=(.10,.09,.075,1)
MUTED=(.34,.30,.25,1)


@lru_cache(maxsize=512)
def text_height(text,width,font,size,bold=False):
    label=CoreLabel(text=text,text_size=(max(1,width),None),font_name=font,font_size=size,bold=bold,line_height=1.0)
    label.refresh()
    return label.texture.size[1]


class NewspaperScreen(FloatLayout):
    def __init__(self,menu):
        super().__init__()
        self.menu=menu;self.loc=menu.game.i18n;self.scroll=None
        with self.canvas.before:
            Color(.96,.935,.875,1);self.paper=Rectangle(pos=self.pos,size=self.size)
        self.back=MenuTile('BACK',lambda:menu.action('hub'));self.back.size_hint=(None,None);self.add_widget(self.back)
        self.masthead=self.label('SCORER DAILY',font='assets/fonts/BarlowCondensed-ExtraBoldItalic.ttf',bold=True)
        self.dateline=self.label('',color=MUTED)
        self.headline=self.label('',bold=True)
        self.score=self.label('',bold=True)
        self.body=self.label('')
        self.caption=self.label(self.loc.tr('Match illustration'),color=MUTED)
        c=menu.game.career;self.report=current_report(c)
        self.photo=None
        if self.report is None:
            self.body.text=self.loc.tr('Your first match report will appear here after you play.')
        else:
            r=self.report
            def team(entry,side):
                uid=entry.get(side+'_uid','')
                if uid.startswith('nation:'):return self.loc.country(uid[7:])
                club=next((cl for league in c.leagues.values() for cl in league.clubs if cl.uid==uid),None) if uid else None
                return c.display_club(club) if club else c.display_text(entry.get(side,''),entry.get('country'))
            competition=self.loc.competition(c,r['competition'],r['country'])
            self.article=article(r,self.loc.tr,team,c.player_name,competition)
            self.short_headline=team(r,'home')+' · '+team(r,'away')
            self.full_text='\n\n'.join(self.article['paragraphs'][1:])
            self.brief_text=brief_article(r,self.loc.tr,c.player_name)
            self.dateline.text=r['date']+' · '+str(competition)
            self.headline.text=self.article['headline'];self.headline.font_name=self.loc.font(self.headline.text);self.dateline.font_name=self.loc.font(self.dateline.text);self.score.text=self.loc.tr(r['status'])
            self.photo=Image(source=self.article['photo'],size_hint=(None,None),fit_mode='contain');self.add_widget(self.photo)
        self._layout_trigger=Clock.create_trigger(self._layout,0)
        self.bind(pos=self._layout_trigger,size=self._layout_trigger)
        self._layout_trigger()

    def label(self,text,bold=False,color=INK,font=None):
        w=Label(text=text,color=color,bold=bold,font_name=font or self.loc.font(text),size_hint=(None,None),halign='left',valign='top',shorten=False)
        self.add_widget(w);return w

    def measure(self,w,text,width,size):
        return text_height(str(text),int(width),w.font_name,round(sp(size),2),w.bold)

    def place(self,w,text,x,top,width,size):
        height=self.measure(w,text,width,size)
        w.text=text;w.font_size=sp(size);w.pos=(x,top-height);w.size=(width,height);w.text_size=(width,height)
        return height

    def _layout(self,*_):
        self.paper.pos,self.paper.size=self.pos,self.size
        pad=dp(6);gap=dp(5);left=self.x+pad;right=self.right-pad;width=max(dp(1),self.width-2*pad)
        top=self.top-pad;self.back.pos=(right-dp(88),top-dp(48));self.back.size=(dp(88),dp(48))
        self.place(self.masthead,'SCORER DAILY',left,top-dp(8),max(dp(1),width-dp(96)),20 if width>=dp(360) else 16)
        top-=dp(52)
        self.layout_fits=True
        if self.report is None:
            self.place(self.body,self.body.text,left,top,width,16);return
        self.headline.text=self.article['headline']
        date_h=self.place(self.dateline,self.dateline.text,left,top,width,10)
        top-=date_h+gap
        height=max(dp(1),top-(self.y+pad))
        font=self.loc.font(self.full_text)
        self.body.font_name=font if 'NotoSansCJK' in str(font) else 'assets/fonts/LiberationSerif-Regular.ttf'
        # Try generous type first, then a concise edition. All text remains
        # present in the chosen edition; no hidden lines or text truncation.
        chosen=None
        for concise,text in ((False,self.full_text),(True,self.brief_text)):
            for size in (18,17,16,15,14,13,12):
                heading=size+3
                for photo_width in (min(dp(210),width*.28),min(dp(120),width*.23),min(dp(60),width*.17)):
                    if width>=dp(520):
                        text_width=width-photo_width-gap*2
                        hh=self.measure(self.headline,self.headline.text,text_width,heading)
                        sh=self.measure(self.score,self.score.text,text_width,13)
                        bh=self.measure(self.body,text,text_width,size)
                        required=hh+sh+bh+gap*2
                        fits=required<=height and photo_width*2/3+dp(18)<=height
                        mode='columns'
                    else:
                        text_width=width-photo_width-gap
                        hh=self.measure(self.headline,self.headline.text,text_width,heading)
                        sh=self.measure(self.score,self.score.text,text_width,12)
                        band=max(hh+sh+gap,photo_width*2/3)
                        bh=self.measure(self.body,text,width,size)
                        required=band+gap+bh
                        fits=required<=height
                        mode='stack'
                    if fits:
                        chosen=(concise,text,size,heading,photo_width,mode,text_width,hh,sh,bh);break
                if chosen:break
            if chosen:break
        if chosen is None:
            # Extreme user aliases/font scaling get more usable width by
            # reducing only the illustration, never hiding article text.
            text=self.brief_text.rsplit('\n',1)[-1] if self.article['mentions_player'] else self.brief_text
            self.headline.text=self.short_headline
            size=12;heading=12;photo_width=dp(40);mode='fullwidth';text_width=width
            hh=self.measure(self.headline,self.headline.text,text_width,heading);sh=self.measure(self.score,self.score.text,text_width,12);bh=self.measure(self.body,text,width,size)
            chosen=(True,text,size,heading,photo_width,mode,text_width,hh,sh,bh)
        concise,text,size,heading,pw,mode,tw,hh,sh,bh=chosen
        self.concise=concise;self.body_font_size=size
        self.photo.size=(pw,pw*2/3)
        if mode=='fullwidth':
            h=self.place(self.headline,self.headline.text,left,top,width,heading)
            bar_top=self.top-pad
            self.photo.pos=(right-dp(88)-gap-pw,bar_top-dp(8)-self.photo.height)
            self.place(self.masthead,'SCORER DAILY',left,bar_top-dp(8),dp(94),14)
            score_x=left+dp(98)
            self.place(self.score,self.score.text,score_x,bar_top-dp(8),max(dp(32),self.photo.x-gap-score_x),10)
            self.place(self.body,text,left,top-h-gap,width,size)
            self.caption.opacity=0;self.caption.size=(0,0)
            bottom=self.body.y
        elif mode=='columns':
            self.caption.opacity=1
            self.photo.pos=(left,top-self.photo.height)
            tx=left+pw+gap*2
            h=self.place(self.headline,self.headline.text,tx,top,tw,heading)
            s=self.place(self.score,self.score.text,tx,top-h-gap,tw,13)
            self.place(self.body,text,tx,top-h-s-gap*2,tw,size)
            self.place(self.caption,self.caption.text,left,self.photo.y-gap,pw,9)
            bottom=min(self.body.y,self.caption.y)
        else:
            self.photo.pos=(right-pw,top-self.photo.height)
            h=self.place(self.headline,self.headline.text,left,top,tw,heading)
            s=self.place(self.score,self.score.text,left,top-h-gap,tw,12)
            band=max(h+s+gap,self.photo.height)
            self.place(self.body,text,left,top-band-gap,width,size)
            self.caption.opacity=0;self.caption.size=(0,0)
            bottom=self.body.y
        self.layout_fits=bottom>=self.y+pad-1
