"""Per-season explicit publication choice; names never rename the local career."""
def decline(c):
    from season_review import dismiss
    old=c.season_review.get('share_choice','unasked');c.season_review['share_choice']='declined'
    if dismiss(c):return True
    c.season_review['share_choice']=old;return False

def approve(c,board,name):
    from season_review import dismiss
    report=c.season_review
    keys=board.enqueue_season(report.get('public_records',[]),name)
    old=report.get('share_choice','unasked');report['share_choice']='queued'
    if dismiss(c):return True
    report['share_choice']=old;board.cancel_jobs(keys);return False

def ask_name(menu):
    from kivy.uix.popup import Popup
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.textinput import TextInput
    from kivy.metrics import dp
    from kivy.clock import Clock
    from menu_ui import FlowLabel,TouchButton
    g=menu.game;t=g.i18n.tr;r=g.career.season_review
    if getattr(g,'_season_share_popup',None):return
    body=BoxLayout(orientation='vertical',padding=dp(12),spacing=dp(8))
    body.add_widget(FlowLabel(text=t('Only your chosen name and league goals will appear publicly. This choice applies to this season only.'),localize=False))
    for record in r.get('public_records',[]):
        body.add_widget(FlowLabel(text=t('Division {tier}',tier=record['division'])+' · '+t('{goals} goals',goals=record['goals']),localize=False))
    field=TextInput(text='',hint_text=t('Name for the leaderboard'),font_name=g.i18n.font(t('Name for the leaderboard')),multiline=False,size_hint_y=None,height=dp(48));body.add_widget(field)
    error=FlowLabel(text='');body.add_widget(error)
    buttons=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(8));body.add_widget(buttons)
    popup=Popup(title=t('Publish this season?'),content=body,size_hint=(.92,.85),auto_dismiss=False)
    def confirm(*_):
        try:
            if not approve(g.career,g.leaderboard,field.text):error.text=t('Unable to save your career. Please try again.');return
        except (ValueError,OSError):error.text=t('Enter a valid public name.');return
        popup.dismiss();menu._signature=None;g.draw()
        g.leaderboard.flush_approved(lambda:Clock.schedule_once(lambda _:g.draw(),0))
    buttons.add_widget(TouchButton(t('CANCEL'),popup.dismiss));buttons.add_widget(TouchButton(t('PUBLISH'),confirm,accent=True))
    popup.name_field=field;popup.confirm=confirm
    popup.bind(on_dismiss=lambda *_:setattr(g,'_season_share_popup',None));g._season_share_popup=popup;popup.open()
