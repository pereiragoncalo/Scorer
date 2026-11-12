"""Non-dismissable update gate; only a fixed official Play listing can be opened."""
from kivy.clock import Clock
from kivy.metrics import dp,sp
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from app_updates import UpdateState,installed_version
from version_policy import STORE_URL


def open_store():
    from kivy.utils import platform
    if platform=='android':
        from android.runnable import run_on_ui_thread
        @run_on_ui_thread
        def launch():
            from jnius import autoclass
            intent=autoclass('android.content.Intent');uri=autoclass('android.net.Uri')
            activity=autoclass('org.kivy.android.PythonActivity').mActivity
            try:activity.startActivity(intent(intent.ACTION_VIEW,uri.parse('market://details?id=com.clemir.scorerworld')))
            except Exception:activity.startActivity(intent(intent.ACTION_VIEW,uri.parse(STORE_URL)))
        launch()
    else:
        import webbrowser
        webbrowser.open(STORE_URL)

class UpdateGate:
    def __init__(self,app,path):
        self.app=app;self.state=UpdateState(installed_version(),path);self.popup=None;self.closed=False;self.hint=None;self.hint_event=None
    @property
    def locked(self):return self.state.required
    def check(self):
        self.state.installed=installed_version()
        return self.state.check_async(self.render,lambda f:Clock.schedule_once(lambda _:f(),0))
    def _hint(self,*_):
        if self.hint:
            self.hint.opacity=1 if self.app.root.view=='splash' else 0
            self.hint.size=(max(dp(1),self.app.root.width-dp(24)),dp(24))
            self.hint.text_size=self.hint.size
    def _clear_hint(self):
        if self.hint_event:self.hint_event.cancel();self.hint_event=None
        if self.hint:
            if self.hint.parent:self.hint.parent.remove_widget(self.hint)
            self.hint=None
    def render(self):
        if self.closed:return
        from menu_ui import CreationTile,DashboardField
        from localization import using
        if self.state.checking and not self.state.required:
            if self.hint is None:
                from kivy.core.window import Window
                from kivy.uix.label import Label
                self.hint=Label(text=self.app.root.i18n.tr('Checking for updates'),color=(1,1,1,1),font_size=sp(11),halign='left',valign='middle',size_hint=(None,None),pos=(dp(12),dp(8)))
                Window.add_widget(self.hint);self.hint_event=Clock.schedule_interval(self._hint,.2)
            self._hint();return
        self._clear_hint()
        with using(self.app.root.i18n):
            if not self.locked:
                if self.popup:self.popup.dismiss();self.popup=None
                return
            if self.popup:self.popup.dismiss()
            panel=BoxLayout(orientation='vertical',spacing=dp(12),padding=dp(16))
            title='Update required';detail='A newer version of Scorer is required to continue.'
            panel.add_widget(DashboardField(compact_text=self.app.root.i18n.tr(title),text=self.app.root.i18n.tr(title),localize=False,font_size=sp(20),halign='center',max_lines=0))
            panel.add_widget(DashboardField(compact_text=self.app.root.i18n.tr(detail),text=self.app.root.i18n.tr(detail),localize=False,font_size=sp(14),halign='center',max_lines=0))
            buttons=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(8))
            buttons.add_widget(CreationTile('UPDATE',lambda:open_store(),accent=True))
            retry=CreationTile('RETRY',self.check);retry.disabled=self.state.checking;buttons.add_widget(retry)
            buttons.add_widget(CreationTile('EXIT',self.app.stop));panel.add_widget(buttons)
            self.popup=ModalView(auto_dismiss=False,size_hint=(.88,.72),background_color=(.025,.065,.08,1))
            self.popup.add_widget(panel);self.popup.open()
    def close(self):
        self.closed=True;self._clear_hint()
        if self.popup:self.popup.dismiss();self.popup=None
