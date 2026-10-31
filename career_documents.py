"""User-selected career documents; Android SAF / native Kivy desktop chooser."""
from pathlib import Path
from career_transfer import MAX_BYTES

class CareerDocuments:
    def __init__(self,on_import,on_message):self.on_import=on_import;self.on_message=on_message;self.busy=False;self.export_text=None
    def pick(self,text=None):
        from kivy.utils import platform
        if self.busy:return
        if platform=='android':self._android(text)
        else:self._desktop(text)
    def _android(self,text):
        try:
            from android import activity
            from jnius import autoclass
            self.host=autoclass('org.kivy.android.PythonActivity').mActivity;self.bridge=autoclass('com.clemir.striker.files.LocalNameFiles')
            self.export_text=text;self.busy=True;activity.bind(on_activity_result=self.result)
            if text is None:self.bridge.chooseCareerImport(self.host)
            else:self.bridge.chooseCareerExport(self.host)
        except Exception:
            if 'activity' in locals():activity.unbind(on_activity_result=self.result)
            self.busy=False;self.on_message('File picker unavailable on this device.')
    def result(self,request,result,data):
        if request not in (7243,7244) or not self.busy:return
        from android import activity
        from kivy.clock import Clock
        from threading import Thread
        activity.unbind(on_activity_result=self.result)
        if result!=-1 or data is None:self.busy=False;return
        text=self.export_text
        def complete(message=None,imported=None):
            self.busy=False
            if imported is not None:self.on_import(imported)
            elif message:self.on_message(message)
        def work():
            try:
                if request==7243:
                    imported=str(self.bridge.readCareer(self.host,data.getData()));Clock.schedule_once(lambda _:complete(imported=imported))
                else:
                    self.bridge.writeCareer(self.host,data.getData(),text);Clock.schedule_once(lambda _:complete('Career exported. Keep the file safe before uninstalling.'))
            except Exception:Clock.schedule_once(lambda _:complete('Could not read or write this document. No career changed.'))
        Thread(target=work,daemon=True).start()
    def _desktop(self,text):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.filechooser import FileChooserListView
        from ui_localization import LocalizedPopup,LocalizedInput
        from menu_ui import TouchButton
        from kivy.metrics import dp
        box=BoxLayout(orientation='vertical',spacing=dp(8));chooser=FileChooserListView(path=str(Path.home()),filters=['*.json']);box.add_widget(chooser)
        filename=LocalizedInput(text='scorer-career.json',multiline=False,size_hint_y=None,height=dp(48));box.add_widget(filename)
        actions=BoxLayout(size_hint_y=None,height=dp(48));box.add_widget(actions)
        popup=LocalizedPopup(title='Career document',content=box,size_hint=(.95,.95));self.busy=True
        def done(*_):self.busy=False
        popup.bind(on_dismiss=done)
        def perform(*_):
            try:
                if text is None:
                    if not chooser.selection:return
                    path=Path(chooser.selection[0])
                    if path.stat().st_size>MAX_BYTES:raise ValueError()
                    value=path.read_text(encoding='utf8');popup.dismiss();self.on_import(value)
                else:
                    name=filename.text.strip()
                    if not name or Path(name).name!=name or not name.endswith('.json'):raise ValueError()
                    path=Path(chooser.path)/name
                    # Refuse overwrite; the user can choose another filename.
                    with path.open('x',encoding='utf8') as f:f.write(text)
                    popup.dismiss();self.on_message('Career exported. Keep the file safe before uninstalling.')
            except (OSError,ValueError):self.on_message('Could not read or write this document. No career changed.')
        actions.add_widget(TouchButton('CANCEL',popup.dismiss));actions.add_widget(TouchButton('IMPORT CAREER' if text is None else 'EXPORT CAREER',perform));popup.open()
