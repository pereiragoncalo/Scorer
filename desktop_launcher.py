"""Scorer Free Windows launcher: resource cwd and persistent per-user career."""
import json
import os
from pathlib import Path
import sys


def configure(resources=None):
    root = Path(resources or getattr(sys, '_MEIPASS', Path(__file__).resolve().parent)).resolve()
    if not (root/'assets/icon.png').is_file():
        raise RuntimeError('Scorer assets are missing from this installation')
    local = Path(os.environ.get('LOCALAPPDATA') or Path.home()/'AppData/Local')
    directory = Path(os.environ.get('STRIKER_SAVE_DIR') or local/'Clemir/Scorer/Free').resolve()
    directory.mkdir(parents=True, exist_ok=True)
    os.environ['STRIKER_SAVE_DIR'] = str(directory)
    os.environ.setdefault('KIVY_HOME', str(directory/'kivy'))
    os.environ['KIVY_NO_ARGS'] = '1'
    if sys.platform == 'win32':
        os.environ.setdefault('KIVY_GL_BACKEND','angle_sdl2')
    os.chdir(root)
    return directory


def main():
    smoke = len(sys.argv) == 3 and sys.argv[1] == '--smoke-test'
    report = Path(sys.argv[2]).resolve() if smoke else None
    if len(sys.argv)>1 and not smoke:
        raise SystemExit('Usage: Scorer-Free.exe [--smoke-test REPORT.json]')
    # Automation must never replace a real player's save.
    if smoke:
        if not os.environ.get('STRIKER_SAVE_DIR'):
            raise SystemExit('Smoke test requires an explicit empty STRIKER_SAVE_DIR')
        if any(Path(os.environ['STRIKER_SAVE_DIR']).glob('*.json')):
            raise SystemExit('Smoke test refuses a nonempty save directory')
    directory = configure()
    import edition
    if edition.WORLD_BUILD or edition.WORLD_PREVIEW:
        raise SystemExit('This launcher requires the fixed Free edition')
    # main applies the initial window dimensions before Window is created.
    from main import StrikerApp
    from kivy.clock import Clock
    from kivy.core.window import Window

    class WindowsApp(StrikerApp):
        def build(self):
            game = super().build()
            def request_close(*_):
                game._request_exit()
                return True  # Preserve the save/error/cancel exit confirmation.
            Window.bind(on_request_close=request_close)
            self._close_callback = request_close
            return game

        def on_stop(self):
            if hasattr(self, '_close_callback'):
                Window.unbind(on_request_close=self._close_callback)
            super().on_stop()

    app = WindowsApp()
    result = {'ok':False,'platform':sys.platform,'frozen':bool(getattr(sys,'frozen',False))}
    if smoke:
        def finish(*_):
            Window.unbind(on_flip=finish)
            try:
                report.parent.mkdir(parents=True,exist_ok=True)
                # GLES/ANGLE guarantees RGBA readback, not SDL's RGB helper.
                from kivy.graphics.opengl import glReadPixels,GL_RGBA,GL_UNSIGNED_BYTE
                from PIL import Image
                width,height=map(int,Window.size)
                pixels=glReadPixels(0,0,width,height,GL_RGBA,GL_UNSIGNED_BYTE)
                Image.frombytes('RGBA',(width,height),pixels).transpose(Image.Transpose.FLIP_TOP_BOTTOM).save(report.with_suffix('.png'))
            except Exception as error:
                result.update(ok=False,error=type(error).__name__+': '+str(error))
            finally:
                report.write_text(json.dumps(result,indent=2),encoding='utf8')
                Clock.schedule_once(lambda _:app.stop(),0)

        def arm_capture(_):
            Window.bind(on_flip=finish)
            Window.canvas.ask_update()

        def exercise(_):
            try:
                g=app.root
                assert g.view == 'splash'
                g._activate_ui('splash_continue')
                assert g.view == 'start'
                g._activate_ui('new_game')
                g._activate_ui('save_profile','Windows Test')
                assert g.view == 'offers' and g.career.offers
                g._activate_ui('accept_offer',g.career.offers[0])
                assert g.view == 'hub' and not g.career.world_unlocked
                g._activate_ui('training');g._activate_ui('training_start')
                for _ in range(3):
                    g.result_text='GOAL!';g._advance_after_shot()
                assert g.career.trained_this_week
                assert g.career.save()
                from career import CareerMode
                restored=CareerMode(autoload=True)
                assert restored.player_name == g.career.player_name
                assert restored.club_name == g.career.club_name
                assert restored.trained_this_week
                assert g.usage.endpoint == '' and not g.usage.enabled
                assert g.ads.backend is None
                assert g.career.save_path.parent == directory
                g.view='hub';g.draw()
                result.update(ok=True,career_reload=True,training=True,free=True,ads_sdk=False)
                app._close_callback()
                assert g._exit_popup is not None
                g._exit_popup.dismiss()
                result['close_confirmation']=True
            except Exception as error:
                result.update(ok=False,error=type(error).__name__+': '+str(error))
            finally:
                # Let Kivy render the changed widget tree before reading pixels.
                Clock.schedule_once(arm_capture,.5)
        Clock.schedule_once(exercise,1.5)
    app.run()
    return 0 if not smoke or result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
