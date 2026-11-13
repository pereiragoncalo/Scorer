"""Season-end review: frozen facts and the completed season's coach portrait."""
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color,RoundedRectangle
from kivy.metrics import dp,sp
from menu_ui import MenuTile,INK,GREEN,MUTED
from coach import PORTRAITS

class SeasonReviewScreen(FloatLayout):
    def __init__(self,menu):
        super().__init__();self.menu=menu;self.loc=menu.game.i18n;self.report=menu.game.career.season_review
        self.items=[]
        self.photo=Image(source=PORTRAITS[self.report['portrait']],fit_mode='contain',size_hint=(None,None));self.add_widget(self.photo)
        self.continue_button=MenuTile('CONTINUE',lambda:menu.action('season_review_done'),accent=True);self.continue_button.size_hint=(None,None);self.add_widget(self.continue_button)
        self.error=self.label('',(1,.65,.45,1))
        with self.canvas.before:
            Color(.025,.08,.10,.98);self.panel=RoundedRectangle(radius=[dp(12)])
        self.bind(pos=self.fit,size=self.fit);self.fit()
        c=menu.game.career
        if getattr(c,'_review_saved',None)!=self.report['season']:
            if c.save() is not False:c._review_saved=self.report['season']
    def label(self,text,color=INK):
        w=Label(text=text,color=color,font_name=self.loc.font(text),size_hint=(None,None),halign='left',valign='top')
        self.add_widget(w);return w
    def fit(self,*_):
        for widget in self.items:self.remove_widget(widget)
        self.items=[];r=self.report;t=self.loc.tr;m=dp(12);gap=dp(14)
        self.panel.pos=(self.x+m/2,self.y+m/2);self.panel.size=(max(1,self.width-m),max(1,self.height-m))
        left=self.x+m;top=self.top-m;width=max(1,self.width-2*m);col=(width-2*gap)/3
        small=self.height<dp(390);dense=self.height<dp(330);fs=10 if dense else 11 if small else 14;row=dp(20 if small else 31)
        def text(value,x,y,w,h,size=fs,heading=False):
            label=self.label(value,GREEN if heading else INK);label.pos=(x,y-h);label.size=(w,h);label.text_size=(w,h);label.font_size=sp(size);self.items.append(label);return label
        text(t('SEASON REVIEW')+f"  {r['season']}/{str(r['season']+1)[-2:]}",left,top,width,dp(31),16 if small else 22,True)
        top-=dp(35 if small else 45)
        text(r['club']+' · '+r['league'],left,top,width,row,fs+1)
        top-=row
        text(t('League finish: {position}/{teams} · {points} pts',**r),left,top,col*2+gap,row)
        text(t('Goals: {goals} · Matches: {matches}',**r),left,top-row,col*2+gap,row)
        stats_top=top-row*2-dp(8)
        def result(key,caption,y):
            text(t(caption),left,y,col,row,heading=True);item=r[key]
            value=t('No recorded result') if not item else f"{item['home']} {item['score']} {item['away']}\n{item['competition']} · {item['date']}"
            text(value,left,y-row,col,row*2.4)
        result('best','BEST RESULT',stats_top);result('worst','WORST RESULT',stats_top-row*3.6)
        x=left+col+gap
        text(t('LEAGUE TOP SCORERS'),x,stats_top,col,row,heading=True)
        y=stats_top-row
        for scorer in r['leaders'][:3 if small else 5]:
            text(f"{scorer['rank']}. {scorer['name']} · {scorer['goals']}",x,y,col,row*1.7);y-=row*1.7
        rank=t('Not ranked') if r['player_rank'] is None else str(r['player_rank'])
        text(t('YOUR POSITION')+f": {rank}\n{r['player']} · {r['player_goals']}",x,y-dp(4),col,row*2,fs)
        x=left+2*(col+gap);photo_h=dp(45 if dense else 70 if small else 130)
        self.photo.pos=(x,top+row-photo_h);self.photo.size=(col,photo_h)
        y=top+row-photo_h-dp(5)
        text(t("COACH'S REVIEW"),x,y,col,row,heading=True);y-=row
        phrases={'strong':'A strong team season. Carry this standard into next year.','poor':'We fell short as a team. We need a stronger response next season.','mixed':'A mixed team season. We must be more consistent.'}
        team_text=t(phrases[r['assessment']])
        if small:
            import re
            team_text=re.split(r'(?<=[.!?。！？])\s*',team_text,maxsplit=1)[0]
        personal=t('You met your scoring target.' if r['target_met'] else 'Your scoring fell short of the target.')
        feedback=team_text+'\n'+(personal if small else t('You scored {goals} goals against a target of {target}.',**r)+' '+personal)
        h=row*(2.5 if dense else 3.2 if small else 3.3);text(feedback,x,y,col,h);y-=h+dp(5)
        text(t('NEXT SEASON'),x,y,col,row,heading=True);y-=row
        target=r['next_goal_target']
        objectives=t('Choose a club before setting next season\'s targets.') if target is None else t('{goals} goals · Coach trust 70/100',goals=target)+('' if dense else '\n'+t('Defend the title.' if r['position']==1 else 'Improve the league finish.'))
        text(objectives,x,y,col,row*(2 if dense else 3 if small else 2.3))
        self.continue_button.pos=(self.right-m-dp(190),self.y+m);self.continue_button.size=(dp(190),dp(48))
        self.error.pos=(left,self.y+m);self.error.size=(max(1,width-dp(205)),dp(48));self.error.text_size=self.error.size;self.error.font_size=sp(fs)
