"""Android Storage Access Framework; returns document text for explicit preview."""
class NameFiles:
    def __init__(self, on_import, on_message):
        self.on_import, self.on_message = on_import, on_message
        self.export_text = ''
        self.busy = False

    def pick(self, text=None):
        try:
            from android import activity
            from jnius import autoclass
            self.host = autoclass('org.kivy.android.PythonActivity').mActivity
            self.bridge = autoclass('com.clemir.striker.files.LocalNameFiles')
            if self.busy:
                return
            self.export_text = text
            self.busy = True
            activity.bind(on_activity_result=self.result)
            if text is None:
                self.bridge.chooseImport(self.host)
            else:
                self.bridge.chooseExport(self.host)
        except Exception:
            if 'activity' in locals():
                activity.unbind(on_activity_result=self.result)
            self.busy = False
            self.on_message('File picker unavailable on this device.')

    def result(self, request, result, data):
        if request not in (7241, 7242) or not self.busy:
            return
        from android import activity
        from kivy.clock import Clock
        activity.unbind(on_activity_result=self.result)
        if result != -1 or data is None:
            self.busy = False
            return
        export_text = self.export_text
        def complete(callback):
            self.busy = False
            callback()
        def work():
            try:
                if request == 7241:
                    text = str(self.bridge.read(self.host, data.getData()))
                    Clock.schedule_once(lambda dt: complete(lambda: self.on_import(text)))
                else:
                    self.bridge.write(self.host, data.getData(), export_text)
                    Clock.schedule_once(lambda dt: complete(lambda: self.on_message('Names template exported. Edit the names, then import it to preview.')))
            except Exception:
                Clock.schedule_once(lambda dt: complete(lambda: self.on_message('Could not read or write this document. No names changed.')))
        from threading import Thread
        Thread(target=work, daemon=True).start()
