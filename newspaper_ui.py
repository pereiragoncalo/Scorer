"""Folded broadsheet in a dark reading window, with real text flow and leaf turns."""
from functools import lru_cache
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color,Rectangle,Line,Triangle
from kivy.metrics import dp,sp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from menu_ui import MenuTile
from newspaper import single_page_story, article,current_report

INK=(.12,.105,.078,1)
MUTED=(.36,.30,.21,1)
PIXEL='assets/fonts/ScorerRetro.ttf'
DISPLAY='assets/fonts/ScorerRetro.ttf'


def press_font(loc,text,title=False):
    return loc.font(text)


@lru_cache(maxsize=768)
def text_height(text,width,font,size,bold=False):
    label=CoreLabel(text=text,text_size=(max(1,int(width)),None),font_name=font,font_size=size,bold=bold,line_height=1.0)
    label.refresh();return label.texture.size[1]


@lru_cache(maxsize=768)
def take_text(text,width,height,font,size):
    """Wrap with Kivy's actual font metrics; retain every non-whitespace character."""
    if not text or width<=0 or height<=0:return '',text,0
    label=CoreLabel(text=text,text_size=(int(width),None),font_name=font,font_size=size,line_height=1.0)
    label.refresh();lines=[];records=[];used=0
    for line in label._cached_lines:
        if used+line.h>height-1:break
        lines.append(''.join(w.text for w in line.words));records.append(line);used+=line.h
    if len(lines)>1 and not records[-1].is_last_line and records[-2].is_last_line:
        lines.pop()
    while lines and not lines[-1].strip():lines.pop()
    if not lines:return '',text,0
    output='\n'.join(lines).rstrip();count=sum(not c.isspace() for c in output)
    found=0;index=0
    while index<len(text) and found<count:
        if not text[index].isspace():found+=1
        index+=1
    return output,text[index:].lstrip(),text_height(output,width,font,size)


class NewspaperScreen(FloatLayout):
    def __init__(self,menu):
        super().__init__();self.menu=menu;self.loc=menu.game.i18n;self.scroll=None;self.page=0;self.pages=[];self.fragments=[]
        self.back=MenuTile('CONTINUE',lambda:menu.action('post_match_continue'));self.back.size_hint=(None,None);self.add_widget(self.back)
        self.help=MenuTile('HELP',lambda:menu.action('help'));self.help.size_hint=(None,None);self.add_widget(self.help)
        self.previous=MenuTile('PREVIOUS',lambda:self.turn(-1));self.previous.size_hint=(None,None)
        self.following=MenuTile('NEXT',lambda:self.turn(1));self.following.size_hint=(None,None)
        self.counter=self.label('',(.84,.84,.76,1))
        self.masthead=self.label('SCORER DAILY',INK,DISPLAY);self.masthead.halign='center'
        self.dateline=self.label('',MUTED);self.headline=self.label('',INK);self.score=self.label('',INK)
        self.caption=None  # Photo is part of the story flow, without a caption.
        self.photo=None;c=menu.game.career;self.report=current_report(c)
        if self.report is None:
            self.story_text=self.loc.tr('Your first match report will appear here after you play.')
            self.full_headline=self.loc.tr('MATCH REPORT');self.date_text='';self.score_text=''
        else:
            r=self.report
            def team(entry,side):
                uid=entry.get(side+'_uid','')
                if uid.startswith('nation:'):return self.loc.country(uid[7:])
                club=next((cl for league in c.leagues.values() for cl in league.clubs if cl.uid==uid),None) if uid else None
                return c.display_club(club) if club else c.display_text(entry.get(side,''),entry.get('country'))
            competition=self.loc.competition(c,r['competition'],r['country'])
            self.article=article(r,self.loc.tr,team,c.player_name,competition)
            limit=8 if self.loc.language in ('ko','ja','zh') else 14
            short=lambda text:text if len(text)<=limit else text[:limit-3]+'...'
            self.fixture_text=short(team(r,'home'))+'  '+str(r['status'])+'  '+short(team(r,'away'))
            pieces=[self.article['lead']]
            if self.article['goals']:pieces.append(' '.join(e['text'] for e in self.article['goals']))
            pieces.append(self.loc.tr('MATCH SUMMARY')+': '+self.article['summary'])
            if self.article['mention']:pieces.append(self.article['mention'])
            self.story_text='\n\n'.join(pieces)
            self.compact_story_text='\n\n'.join(pieces[1:])
            self.full_headline=self.article['headline'];self.date_text=r['date']+'  /  '+str(competition);self.score_text=self.loc.tr(r['status'])
            self.photo=Image(source=self.article['photo'],size_hint=(None,None),fit_mode='contain');self.add_widget(self.photo)
        self.short_story_text=single_page_story(self.report,self.loc.tr,c.player_name) if self.report else self.story_text
        self.full_story_text=self.story_text
        self._layout_trigger=Clock.create_trigger(self._layout,0)
        self.bind(pos=self._layout_trigger,size=self._layout_trigger);self._layout_trigger()

    def label(self,text,color=INK,font=None):
        label=Label(text=text,color=color,font_name=font or press_font(self.loc,text),size_hint=(None,None),halign='left',valign='top',shorten=False)
        self.add_widget(label);return label

    def place(self,label,text,x,top,width,size,font=None):
        label.font_name=font or press_font(self.loc,text)
        height=text_height(str(text),int(width),label.font_name,sp(size))
        label.text=text;label.font_size=sp(size);label.pos=(x,top-height);label.size=(width,height);label.text_size=(int(width),height)
        return height

    def triangle(self,points,color):
        Color(*color);Triangle(points=points)

    def _draw_paper(self,x,y,w,h):
        self.canvas.before.clear()
        with self.canvas.before:
            from kivy.core.image import Image as CoreImage
            if not hasattr(self,'_paper_sprite'):
                self._paper_sprite=CoreImage('assets/sprites/scene/newspaper.png').texture
                self._paper_sprite.mag_filter=self._paper_sprite.min_filter='nearest'
            Color(.025,.045,.052,1);Rectangle(pos=self.pos,size=self.size)
            Color(1,1,1,1);Rectangle(texture=self._paper_sprite,pos=(x-dp(10),y-dp(9)),size=(w+dp(28),h+dp(24)))

    def turn(self,step):
        self.page=max(0,min(len(self.pages)-1,self.page+step));self._layout_trigger()

    def _regions(self,left,top,width,height,size,first):
        gap=dp(16);columns=2 if width>=dp(630) else 1
        col=(width-gap)/2 if columns==2 else width
        regions=[]
        available_photo_height=max(0,min(height*.48,height-dp(24))-dp(8))
        photo_width=max(dp(40),min(dp(200),col*.43,available_photo_height*1.5)) if first and self.photo and available_photo_height>=dp(16) else 0
        photo_height=photo_width*2/3
        band=photo_height+dp(6) if photo_width else 0
        if photo_width:
            regions.append((left+photo_width+dp(10),top,col-photo_width-dp(10),band))
            if height-band>0:regions.append((left,top-band,col,height-band))
        else:regions.append((left,top,col,height))
        if columns==2:regions.append((left+col+gap,top,col,height))
        return regions,photo_width,photo_height

    def _flow(self,text,left,top,width,height,size,first=True):
        font=press_font(self.loc,self.story_text);regions,pw,ph=self._regions(left,top,width,height,size,first)
        parts=[];remaining=text
        for x,t,w,h in regions:
            out,remaining,used=take_text(remaining,int(w),int(h),font,sp(size))
            if out:parts.append(dict(text=out,x=x,top=t,width=w,height=used,font=font,size=size))
        return parts,remaining,pw,ph

    def _layout(self,*_):
        small=self.width<dp(500) or self.height<dp(310)
        dense=self.height<dp(450)
        margin=dp(10) if small else max(dp(36),self.width*.075)
        pw=self.width-2*margin-dp(20);px=self.x+margin;py=self.y+(dp(10) if small else dp(28));ph=self.height-(dp(70) if small else dp(105))
        self.sheet_bounds=(px,py,pw,ph);self._draw_paper(px,py,pw,ph)
        self.back.pos=(self.right-dp(100),self.top-dp(54 if small else 64));self.back.size=(dp(90),dp(48))
        self.help.size=(dp(80),dp(48));self.help.pos=(self.back.x-dp(88),self.back.y)
        inset=dp(10) if small else dp(14) if dense else dp(20);left=px+inset;top=py+ph-inset;width=pw-2*inset
        mh=self.place(self.masthead,'SCORER DAILY',left,top,width,14 if small else 28 if dense else 42,DISPLAY)
        top-=mh+dp(2 if small else 4)
        date=self.report['date'] if small and self.report else self.date_text
        if small and text_height(date,int(width),press_font(self.loc,date),sp(9))>dp(20):date=self.report['date'] if self.report else ''
        dh=self.place(self.dateline,date,left,top,width,9 if small else 10);top-=dh+dp(2 if small else 5)
        title=self.full_headline;title_size=14 if small else 18 if dense else 28
        if small or text_height(title,int(width),press_font(self.loc,title,True),sp(title_size))>ph*.25:
            player=self.menu.game.career.player_name.split()[0]
            limit=7 if self.loc.language in ('ko','ja','zh') else 18
            player=player if len(player)<=limit else player[:limit-3]+'...'
            title=(self.loc.tr('{player}: one goal.',player=player) if self.report and self.report['goals']==1 else self.loc.tr('{player}: {goals} goals.',player=player,goals=self.report['goals']) if self.report and self.report['goals'] else self.loc.tr('MATCH REPORT'));title_size=14
        self.story_text=self.compact_story_text if self.report is not None and dense and title==self.full_headline and date==self.date_text else self.full_story_text
        hh=self.place(self.headline,title,left,top,width,title_size,press_font(self.loc,title,True));top-=hh+dp(2 if small else 4)
        sh=self.place(self.score,self.fixture_text if small and self.report else self.score_text,left,top,width,9 if small else 13);top-=sh+dp(4 if small else 9)
        self.rules=(left,top+dp(4),width)
        with self.canvas.before:
            Color(*INK);Line(points=[left,top+dp(4),left+width,top+dp(4)],width=1)
            Line(points=[left,py+ph-inset-mh-dp(1),left+width,py+ph-inset-mh-dp(1)],width=1.2)
        height=max(dp(18),top-(py+inset));self.layout_fits=True
        if width>=dp(630):
            with self.canvas.before:
                Color(.25,.20,.14,.20);Line(points=[left+width/2,top,left+width/2,py+inset],width=.6)
        selected=None
        for size in ((22,20,18,17,16,15,14,13,12) if not small else (15,14,13,12)):
            parts,remaining,imgw,imgh=self._flow(self.story_text,left,top,width,height,size)
            if not remaining:selected=(size,parts,imgw,imgh);break
        if selected is None:
            self.story_text=self.short_story_text
            for size in (14,13,12,11,10,9,8,7,6):
                parts,remaining,imgw,imgh=self._flow(self.story_text,left,top,width,height,size)
                if not remaining:selected=(size,parts,imgw,imgh);break
        if selected is None:
            # Extremely small windows/high scorelines prioritise the complete
            # concise report over its decorative photograph.
            for size in (12,11,10,9,8,7,6):
                parts,remaining,imgw,imgh=self._flow(self.story_text,left,top,width,height,size,False)
                if not remaining:selected=(size,parts,imgw,imgh);break
        if selected is not None:
            size,parts,imgw,imgh=selected;remaining=''
        pages=[parts]
        self.pages=pages;self.page=min(self.page,len(pages)-1);self.body_font_size=size
        for label in self.fragments:self.remove_widget(label)
        self.fragments=[]
        for part in pages[self.page]:
            label=self.label(part['text'],INK,part['font']);self.place(label,part['text'],part['x'],part['top'],part['width'],size,part['font']);self.fragments.append(label)
            self.layout_fits=self.layout_fits and label.y>=py+inset-1
        self.body=self.fragments[0] if self.fragments else self.label('')
        if self.photo:
            self.photo.opacity=1 if imgw>0 else 0;self.photo.size=(imgw,imgh);self.photo.pos=(left,top-imgh)

        if len(pages)>1:
            for widget in (self.previous,self.following):
                if widget.parent is None:self.add_widget(widget)
            self.previous.pos=(self.x+dp(10),self.top-dp(54));self.previous.size=(dp(72),dp(48));self.previous.disabled=self.page==0
            self.following.pos=(self.x+dp(90),self.top-dp(54));self.following.size=(dp(72),dp(48));self.following.disabled=self.page==len(pages)-1
            self.place(self.counter,f'{self.page+1}/{len(pages)}',self.x+dp(170),self.top-dp(18),dp(48),10);self.counter.opacity=1
        else:
            for widget in (self.previous,self.following):
                if widget.parent:self.remove_widget(widget)
            self.counter.opacity=0
        self.layout_fits=self.layout_fits and not remaining
