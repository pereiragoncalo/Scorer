"""Season-end review: frozen facts and the completed season's coach portrait."""
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color,RoundedRectangle
from kivy.metrics import dp,sp
from kivy.core.text import Label as CoreLabel
from menu_ui import MenuTile,INK,GREEN,MUTED
from coach import PORTRAITS

class SeasonReviewScreen(FloatLayout):
    def __init__(self,menu):
        super().__init__();self.menu=menu;self.loc=menu.game.i18n;self.report=menu.game.career.season_review
        self.items=[]
        self.photo=Image(source=PORTRAITS[self.report['portrait']],fit_mode='contain',size_hint=(None,None));self.add_widget(self.photo)
        self.can_share=bool(self.report.get('public_records'))
        self.continue_button=MenuTile('DO NOT PUBLISH' if self.can_share else 'CONTINUE',lambda:menu.action('season_decline' if self.can_share else 'season_review_done'),accent=not self.can_share);self.continue_button.size_hint=(None,None);self.add_widget(self.continue_button)
        self.publish_button=None
        if self.can_share:
            from season_sharing import ask_name
            self.publish_button=MenuTile('PUBLISH THIS SEASON',lambda:ask_name(menu),accent=True);self.publish_button.size_hint=(None,None);self.add_widget(self.publish_button)
        self.error=self.label('',(1,.65,.45,1))
        with self.canvas.before:
            Color(.025,.08,.10,.98);self.panel=RoundedRectangle(radius=[dp(12)])
            Color(.045,.105,.13,1);self.review_cards=[RoundedRectangle(radius=[dp(8)]) for _ in range(3)]
        self.bind(pos=self.fit,size=self.fit);self.fit()
        c=menu.game.career
        if getattr(c,'_review_saved',None)!=self.report['season']:
            if c.save() is not False:c._review_saved=self.report['season']
    def label(self,text,color=INK):
        w=Label(text=text,color=color,font_name=self.loc.font(text),size_hint=(None,None),halign='left',valign='top')
        self.add_widget(w);return w
    def fit(self,*_):
        for widget in self.items:self.remove_widget(widget)
        self.items=[];r=self.report;t=self.loc.tr
        compact=self.height<dp(420);dense=self.height<dp(330);m=dp(10 if compact else 18);gap=dp(12)
        self.panel.pos=(self.x+m/2,self.y+m/2);self.panel.size=(max(1,self.width-m),max(1,self.height-m))
        left=self.x+m;right=self.right-m;top=self.top-m;width=max(1,right-left)
        header=dp(88 if compact else 116);footer=dp(60)
        body_top=top-header;body_bottom=self.y+m+footer
        body_height=max(dp(110),body_top-body_bottom);col=(width-2*gap)/3
        fs=10 if self.height<dp(330) else 11 if compact else 14
        def text(value,x,y,w,h,size=fs,heading=False):
            label=self.label(value,GREEN if heading else INK);label.pos=(x,y-h);label.size=(w,h);label.text_size=(w,h);label.font_size=sp(size)
            label.shorten=False;label.padding=(dp(2),0)
            fitted=size
            while fitted>9:
                measure=CoreLabel(text=value,font_name=label.font_name,font_size=sp(fitted),text_size=(max(1,w-dp(4)),None));measure.refresh()
                if measure.texture.size[1]<=h:break
                fitted-=.5
            label.font_size=sp(fitted)
            measure=CoreLabel(text=value,font_name=label.font_name,font_size=sp(fitted),text_size=(max(1,w-dp(4)),None));measure.refresh();label._natural_height=measure.texture.size[1]
            self.items.append(label);return label
        text(t('SEASON REVIEW')+f"  {r['season']}/{str(r['season']+1)[-2:]}",left,top,width,dp(25 if compact else 32),16 if compact else 22,True)
        y=top-dp(29 if compact else 40)
        text(r['club']+' · '+r['league'],left,y,width,dp(23 if compact else 30),fs+1)
        y-=dp(24 if compact else 32)
        text(t('League finish: {position}/{teams} · {points} pts',**r)+'    '+t('Goals: {goals} · Matches: {matches}',**r),left,y,width,dp(24),fs)
        heading=dp(16 if dense else 20 if compact else 26);pad=dp(4 if dense else 8)
        for i,card in enumerate(self.review_cards):card.pos=(left+i*(col+gap)-dp(3),body_bottom-dp(3));card.size=(col+dp(6),body_height+dp(6))
        def result(key,caption,y,h):
            text(t(caption),left,y,col,heading,heading=True)
            item=r[key]
            if item:
                value=f"{item['home']} {item['score']} {item['away']}"
                detail=item['date']
                detail_h=dp(13 if dense else 17)
                value_h=max(1,h-heading-detail_h-dp(3))
                name=text(value,left,y-heading,col,value_h)
                text(detail,left,y-heading-min(value_h,name._natural_height)-dp(3),col,detail_h,max(9,fs-1))
            else:text(t('No recorded result'),left,y-heading,col,h-heading)
        result('best','BEST RESULT',body_top,body_height/2-pad)
        result('worst','WORST RESULT',body_top-body_height/2,body_height/2-pad)
        x=left+col+gap
        text(t('LEAGUE TOP SCORERS'),x,body_top,col,heading,heading=True)
        own_h=dp(40 if compact else 54);available=max(dp(36),body_height-heading-own_h-pad)
        count=min(len(r['leaders']),3 if compact else 5);row_h=min(dp(42 if compact else 52),available/max(1,count))
        y=body_top-heading
        for scorer in r['leaders'][:count]:
            text(f"{scorer['rank']}. {scorer['name']} · {scorer['goals']}",x,y,col,row_h);y-=row_h
        rank=t('Not ranked') if r['player_rank'] is None else str(r['player_rank'])
        text(t('YOUR POSITION')+f": {rank} · {r['player_goals']}\n{r['player']}",x,max(body_bottom+own_h,y-pad),col,own_h,fs)
        x=left+2*(col+gap);photo_h=min(body_height*.30,dp(80 if compact else 115))
        self.photo.pos=(x,body_top-photo_h);self.photo.size=(col*.44,photo_h)
        text(t("COACH'S REVIEW"),x+col*.47,body_top,col*.53,photo_h,fs,True)
        y=body_top-photo_h-dp(6)
        phrases={'strong':'A strong team season. Carry this standard into next year.','poor':'We fell short as a team. We need a stronger response next season.','mixed':'A mixed team season. We must be more consistent.'}
        team=t(phrases[r['assessment']])
        if compact:
            import re
            team=re.split(r'(?<=[.!?。！？])\s*',team,maxsplit=1)[0]
        feedback=team+' '+t('You met your scoring target.' if r['target_met'] else 'Your scoring fell short of the target.')
        remaining=max(dp(55),y-body_bottom);feedback_h=remaining*.54
        text(feedback,x,y,col,feedback_h);y-=feedback_h
        text(t('NEXT SEASON'),x,y,col,heading,heading=True);y-=heading
        target=r['next_goal_target']
        objectives=t('Choose a club before setting next season\'s targets.') if target is None else t('{goals} goals · Coach trust 70/100',goals=target)
        text(objectives,x,y,col,max(dp(24),y-body_bottom))
        bw=min(dp(220),(width-gap)/2)
        self.continue_button.size=(bw,dp(48));self.continue_button.pos=(right-bw,self.y+m)
        if self.publish_button is not None:
            self.publish_button.size=(bw,dp(48));self.publish_button.pos=(right-2*bw-gap,self.y+m)
        self.error.pos=(left,self.y+m);self.error.size=(max(1,width-(2*bw+gap if self.can_share else bw+gap)),dp(48));self.error.text_size=self.error.size;self.error.font_size=sp(fs)
