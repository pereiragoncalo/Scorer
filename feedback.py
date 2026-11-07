"""Open a user-controlled email draft; never transmit feedback automatically."""
from urllib.parse import quote,urlencode
import release_settings

def mail_url():
    return 'mailto:'+quote(release_settings.SUPPORT_EMAIL,safe='@.+-')+'?'+urlencode({'subject':'Scorer World - Feedback'},quote_via=quote)

def compose(on_failure):
    from kivy.utils import platform
    from kivy.clock import Clock
    def failed():Clock.schedule_once(lambda _dt:on_failure(),0)
    try:
        if platform=='android':
            from android.runnable import run_on_ui_thread
            @run_on_ui_thread
            def launch():
                try:
                    from jnius import autoclass
                    intent=autoclass('android.content.Intent')
                    uri=autoclass('android.net.Uri')
                    activity=autoclass('org.kivy.android.PythonActivity').mActivity
                    activity.startActivity(intent(intent.ACTION_SENDTO,uri.parse(mail_url())))
                except Exception:failed()
            launch()
        else:
            import webbrowser
            if not webbrowser.open(mail_url()):failed()
    except Exception:failed()

def unavailable(game):
    from localization import using
    with using(game.i18n):return _unavailable(game)

def _unavailable(game):
    from kivy.core.window import Window
    from kivy.core.clipboard import Clipboard
    from kivy.uix.boxlayout import BoxLayout
    from kivy.metrics import dp,sp
    from menu_ui import MenuTile,DashboardField,LocalizedPopup
    from ui_localization import LocalizedInput as TextInput
    old=getattr(game,'_feedback_popup',None)
    if old:return
    body=BoxLayout(orientation='vertical',spacing=dp(8))
    text=game.i18n.tr('No email app is available. Send your suggestion to:')
    message=DashboardField(compact_text=text,text=text,localize=False,font_size=sp(13),halign='center',max_lines=0);body.add_widget(message)
    body.add_widget(TextInput(text=release_settings.SUPPORT_EMAIL,readonly=True,multiline=False,size_hint_y=None,height=dp(48),font_size=sp(14)))
    row=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(8));body.add_widget(row)
    popup=LocalizedPopup(title='FEEDBACK',content=body,size_hint=(None,None),size=(min(dp(480),Window.width-dp(24)),min(dp(260),Window.height-dp(24))))
    row.add_widget(MenuTile('COPY EMAIL',lambda:Clipboard.copy(release_settings.SUPPORT_EMAIL)));row.add_widget(MenuTile('CLOSE',popup.dismiss))
    game._feedback_popup=popup;popup.bind(on_dismiss=lambda *_:setattr(game,'_feedback_popup',None));popup.open()
