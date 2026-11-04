"""One-screen coach meeting: measured type, portrait and fixed completion action."""
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color,RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp,sp
from menu_ui import MenuTile,INK,MUTED,GREEN
from coach import conversation_text,FEEDBACK,ROUTINE,STYLES

ADVICE=('Keep calm. Practise low and high finishes.',
        'Build on that performance. Keep varying your finishes.',
        'Review your chances. Work on your timing in training.')
FOLLOW=('I believe in you. Take it one chance at a time.',
        'Keep your focus. I expect a disciplined response.',
        'Prepare consistently and put the lessons into practice.')

class CoachScreen(FloatLayout):
    def __init__(self,menu):
        super().__init__();self.menu=menu;self.loc=menu.game.i18n;c=menu.game.career
        self.meeting=c.coach_conversation();self.scroll=None
        self.full_text=self.loc.tr(conversation_text(self.meeting));m=self.meeting
        opening=ROUTINE[m['variant']%len(ROUTINE)] if m['kind']=='routine' else FEEDBACK[m['kind']][m['style']][m['variant']%len(FEEDBACK[m['kind']][m['style']])]
        advice=ADVICE[0 if m['kind']=='drought' else 1 if m['kind'] in ('decisive','form') else 2]
        self.short_text='\n\n'.join(self.loc.tr(t) for t in (opening,advice,FOLLOW[m['style']]))
        self.title=self.label(self.loc.tr('COACH MEETING'),GREEN)
        self.style_text=self.loc.tr(STYLES[m['style']])
        self.style=self.label(self.style_text,MUTED)
        recent=c._current_coach_state()['recent']
        self.recent=self.label(self.loc.tr('Recent club form: {goals} goals in {games} appearances.',goals=sum(recent),games=len(recent)) if recent else '',MUTED)
        self.feedback=self.label(self.full_text,INK)
        self.portrait=Image(source=c.coach_portrait,fit_mode='contain',size_hint=(None,None));self.add_widget(self.portrait)
        self.error=self.label(c.message if c.message=='Unable to save the meeting. Please try again.' else '',(1,.65,.45,1))
        self.finish=MenuTile('FINISH MEETING',lambda:menu.action('coach_complete'),accent=True);self.finish.size_hint=(None,None);self.add_widget(self.finish)
        with self.canvas.before:
            Color(.035,.10,.11,.98);self.panel=RoundedRectangle(radius=[dp(12)])
        self.trigger=Clock.create_trigger(self.fit,0);self.bind(pos=self.trigger,size=self.trigger);self.trigger()
    def label(self,text,color):
        label=Label(text=text,font_name=self.loc.font(text),size_hint=(None,None),halign='left',valign='top',color=color)
        self.add_widget(label);return label
    def place(self,label,x,y,w,h,size):
        label.pos=(x,y);label.size=(w,h);label.text_size=(w,h);label.font_size=sp(size)
    def fit(self,*_):
        compact=self.height<dp(330);margin=dp(8 if compact else 16);x=self.x+margin;w=max(1,self.width-2*margin)
        self.panel.pos=(x,self.y+margin);self.panel.size=(w,max(1,self.height-2*margin))
        left=x+margin;right=x+w-margin;top=self.top-2*margin
        header_top=top
        if compact:
            self.place(self.title,left,top-dp(22),right-left-dp(70),dp(22),15);top-=dp(25)
            self.style.text=self.style_text+(' · '+self.recent.text if self.recent.text else '')
            self.place(self.style,left,top-dp(26),right-left-dp(70),dp(26),10);top-=dp(29)
            self.recent.opacity=0
        else:
            self.style.text=self.style_text;self.recent.opacity=1
            self.place(self.title,left,top-dp(26),right-left,dp(26),21);top-=dp(29)
            self.place(self.style,left,top-dp(17),right-left,dp(17),14);top-=dp(19)
            rh=dp(16) if self.recent.text else 0
            self.place(self.recent,left,top-rh,right-left,rh,12);top-=rh+dp(6)
        self.finish.size=(min(dp(320),right-left),dp(48 if compact else 52));self.finish.pos=(right-self.finish.width,self.y+2*margin)
        eh=dp(24) if self.error.text else 0
        self.place(self.error,left,self.finish.top+dp(4),right-left,eh,11)
        bottom=self.finish.top+dp(8)+eh;th=max(dp(20),top-bottom)
        if compact:
            self.portrait.size=(dp(60),dp(40));self.portrait.pos=(right-dp(60),header_top-dp(40))
            tx=left;tw=max(dp(20),right-left)
        else:
            pw=min(dp(220),max(dp(60),(right-left)*.24));self.portrait.size=(pw,min(pw*2/3,th));self.portrait.pos=(left,top-self.portrait.height)
            tx=left+pw+dp(10);tw=max(dp(20),right-tx)
        selected=None
        for text in (self.full_text,self.short_text):
            for size in ((18,17,16,15,14,13,12) if text==self.full_text else (15,14,13,12,11,10,9)):
                measure=CoreLabel(text=text,text_size=(int(tw),None),font_name=self.loc.font(text),font_size=sp(size));measure.refresh()
                if measure.texture.size[1]<=th:
                    selected=(text,size);break
            if selected:break
        text,size=selected or (self.short_text,9)
        self.feedback.text=text;self.feedback.font_name=self.loc.font(text)
        self.place(self.feedback,tx,bottom,tw,th,size)
        self.feedback_font_size=size;self.layout_fits=selected is not None
