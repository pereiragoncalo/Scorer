"""One-screen coach meeting: measured type, portrait and fixed completion action."""
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color,RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp,sp
from menu_ui import MenuTile,INK,MUTED,GREEN
from coach import STYLES

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
        from title_events import pending,needs_focus
        event=pending(c) if menu.game.view=='title_coach' else None
        self.is_title=event is not None;self.is_private=menu.game.view=='private_coach';self.requires_focus=not self.is_private and (not self.is_title or needs_focus(c))
        closing=self.loc.tr('Choose one of these two training focuses for the week.' if self.requires_focus else 'This title belongs to everyone. Enjoy the moment with the supporters.')
        if self.is_private:closing=self.loc.tr('The club has received a transfer offer. Consider your role and the next step in your career.' if c.life['private_meeting']=='offer' else 'You have gone five or more games without a goal. Let us review your movement, composure and finishing together.')
        from coach_feedback import translate
        self.full_text='\n\n'.join((translate(self.loc,c.coach_team_feedback()),c.player_name+': '+translate(self.loc,c.coach_individual_feedback()),closing))
        import re
        first=lambda text:re.split(r'(?<=[.!?。！？])\s*',text,maxsplit=1)[0]
        individual_short=first(translate(self.loc,c.coach_individual_feedback()))
        if c._current_coach_state()['recent'] and c._current_coach_state()['recent'][-1]>=3:
            from coach_feedback import HAT_TRICK_LIVE
            individual_short=self.loc.tr('HAT-TRICK!')+' '+self.loc.tr(HAT_TRICK_LIVE[self.meeting['style']])
        self.short_text='\n\n'.join((first(translate(self.loc,c.coach_team_feedback())),c.player_name+': '+individual_short,closing))
        self.title=self.label(self.loc.tr("CHAMPIONS' TEAM TALK" if self.is_title else 'INDIVIDUAL MEETING' if self.is_private else 'WEEKLY TEAM TALK'),GREEN)
        self.style_text=self.loc.tr(STYLES[self.meeting['style']])
        self.style=self.label(self.style_text,MUTED)
        recent=c._current_coach_state()['recent']
        self.recent=self.label(event['title'] if self.is_title else self.loc.tr('{goals} goals / {games} games · Trust {trust}/100 · {role}',goals=sum(recent),games=len(recent),trust=c.coach_trust,role=self.loc.tr(c.team_role)),MUTED)
        self.feedback=self.label('',INK)
        self.closing=self.label('',INK);self.closing.halign='justify'
        self.portrait=Image(source='assets/coaches/team_talk.png',fit_mode='contain',size_hint=(None,None));self.add_widget(self.portrait)
        from kivy.uix.widget import Widget
        self.avatar=Widget(size_hint=(None,None),opacity=0)
        self.error=self.label(c.message if c.message=='Unable to save the meeting. Please try again.' else '',(1,.65,.45,1))
        self.finish=MenuTile('FINISH TEAM TALK',lambda:menu.action('private_complete' if self.is_private else 'title_coach_complete' if self.is_title else 'coach_complete'),accent=True);self.finish.size_hint=(None,None);self.add_widget(self.finish)
        from player_development import NAMES
        self.options=c.coach_focus_options() if self.requires_focus else ();self.choices=[]
        pick=getattr(menu.game,'_coach_focus_pick',None)
        selected=pick[1] if pick and pick[0]==c.coach_key else None
        for focus in self.options:
            button=MenuTile(NAMES[focus],lambda f=focus:menu.action('coach_focus',f),accent=focus==selected);button.size_hint=(None,None)
            self.choices.append(button);self.add_widget(button)
        self.finish.disabled=self.requires_focus and selected not in self.options
        self.help=MenuTile('HELP',lambda:menu.action('help'));self.help.size_hint=(None,None);self.add_widget(self.help)
        with self.canvas.before:
            Color(.035,.10,.11,.98);self.panel=RoundedRectangle(radius=[dp(12)])
        self.trigger=Clock.create_trigger(self.fit,0);self.bind(pos=self.trigger,size=self.trigger);self.trigger()
    def label(self,text,color):
        label=Label(text=text,font_name=self.loc.font(text),size_hint=(None,None),halign='left',valign='top',color=color)
        self.add_widget(label);return label
    def place(self,label,x,y,w,h,size):
        label.pos=(x,y);label.size=(w,h);label.text_size=(w,h);label.font_size=sp(size)
    def measured_height(self,label,width,size,minimum):
        if not label.text:return 0
        measure=CoreLabel(text=label.text,text_size=(max(1,int(width)),None),font_name=label.font_name,font_size=sp(size))
        measure.refresh()
        return max(dp(minimum),measure.texture.size[1]+dp(2))
    def fit(self,*_):
        compact=self.height<dp(330);dense=self.height<dp(260);margin=dp(4 if dense else 8 if compact else 16);x=self.x+margin;w=max(1,self.width-2*margin)
        self.panel.pos=(x,self.y+margin);self.panel.size=(w,max(1,self.height-2*margin))
        left=x+margin;right=x+w-margin;top=self.top-2*margin
        header_top=top
        self.avatar.opacity=0;self.avatar.size=(dp(60),dp(60));self.avatar.pos=(right-dp(60),top-dp(60))
        if compact:
            title_size=13 if dense else 15
            title_h=self.measured_height(self.title,right-left-dp(4),title_size,18 if dense else 22)
            self.place(self.title,left,top-title_h,right-left-dp(4),title_h,title_size);top-=title_h+dp(3)
            self.style.text=self.style_text+(' · '+self.recent.text if self.recent.text else '')
            style_size=8 if dense else 9
            style_h=self.measured_height(self.style,right-left-dp(4),style_size,18 if dense else 22)
            self.place(self.style,left,top-style_h,right-left-dp(4),style_h,style_size);top-=style_h+dp(3)
            self.recent.opacity=0
        else:
            self.style.text=self.style_text;self.recent.opacity=1
            title_h=self.measured_height(self.title,right-left-dp(4),21,26)
            self.place(self.title,left,top-title_h,right-left-dp(4),title_h,21);top-=title_h+dp(3)
            style_h=self.measured_height(self.style,right-left-dp(4),14,17)
            self.place(self.style,left,top-style_h,right-left-dp(4),style_h,14);top-=style_h+dp(2)
            rh=self.measured_height(self.recent,right-left-dp(4),12,16)
            self.place(self.recent,left,top-rh,right-left-dp(4),rh,12);top-=rh+dp(6)
        self.finish.size=(min(dp(320),right-left-dp(80)),dp(48 if compact else 52));self.finish.pos=(right-self.finish.width,self.y+2*margin)
        self.help.pos=(left,self.finish.y);self.help.size=(dp(72),self.finish.height)
        eh=self.measured_height(self.error,right-left,11,24)
        self.place(self.error,left,self.finish.top+dp(4),right-left,eh,11)
        choice_h=dp(48) if self.choices else 0;choice_y=self.finish.top+dp(6);choice_w=max(1,(right-left-dp(8))/2)
        for i,button in enumerate(self.choices):button.pos=(left+i*(choice_w+dp(8)),choice_y);button.size=(choice_w,choice_h)
        self.place(self.error,left,choice_y+choice_h+dp(2),right-left,eh,11)
        bottom=choice_y+choice_h+dp(8)+eh;th=max(dp(20),top-bottom)
        if compact:
            self.portrait.size=(dp(60),dp(40));self.portrait.pos=(right-dp(60),header_top-dp(40))
            tx=left;tw=max(dp(20),right-left)
        else:
            pw=min(dp(220),max(dp(60),(right-left)*.24));self.portrait.size=(pw,min(pw*2/3,th));self.portrait.pos=(left,top-self.portrait.height)
            tx=left+pw+dp(10);tw=max(dp(20),right-tx)
        selected=None
        portrait_height=self.portrait.height
        gap=dp(4 if compact else 8)
        for text in (self.full_text,self.short_text):
            lead,_,closing=text.rpartition('\n\n')
            for size in ((18,17,16,15,14,13,12) if text==self.full_text else (15,14,13,12,11,10,9,8,7) if dense else (15,14,13,12,11,10,9,8)):
                self.feedback.text=lead;self.feedback.font_name=self.loc.font(lead)
                self.closing.text=closing;self.closing.font_name=self.loc.font(closing)
                lead_h=self.measured_height(self.feedback,tw,size,0)
                closing_h=self.measured_height(self.closing,right-left,size,0)
                photo_h=0 if compact else min(portrait_height,max(dp(36),th-gap-closing_h))
                upper_h=max(lead_h,photo_h)
                if upper_h+gap+closing_h<=th:
                    selected=(size,lead_h,closing_h,upper_h,photo_h);break
            if selected:break
        size,lead_h,closing_h,upper_h,photo_h=selected or (9,lead_h,closing_h,upper_h,photo_h)
        if not compact:
            self.portrait.height=photo_h;self.portrait.y=top-photo_h
        self.place(self.feedback,tx,top-lead_h,tw,lead_h,size)
        self.place(self.closing,left,top-upper_h-gap-closing_h,right-left,closing_h,size)
        self.feedback_font_size=size;self.layout_fits=selected is not None
