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
        def report_and_stop():
            report.parent.mkdir(parents=True,exist_ok=True)
            report.write_text(json.dumps(result,indent=2),encoding='utf8')
            Clock.schedule_once(lambda _:app.stop(),0)

        def capture_training(_):
            try:
                g=app.root
                assert not g._show_stadium_crowd()
                g.export_to_png(str(report.parent/'training.png'))
                result.update(empty_training_stands=True,fullscreen=bool(Window.fullscreen),goalkeeper_scale=g.goalkeeper_scale,
                              shot_speed_multiplier=1.22)
            except Exception as error:
                result.update(ok=False,error=type(error).__name__+': '+str(error))
            finally:report_and_stop()

        def capture_goal(_):
            try:
                g=app.root
                assert g.desktop_windows and g._ball_behind_keeper() and not g.ball.active
                g.export_to_png(str(report.parent/'goal.png'))
                result.update(goal_scene_rendered=True,settled_ball_behind_keeper=True,
                              goal_width=g.goal_width,goal_height=g.goal_height)
            except Exception as error:
                result.update(ok=False,error=type(error).__name__+': '+str(error))
            finally:
                if result.get('ok'):
                    g.shot_context='training';g.draw()
                    Clock.schedule_once(capture_training,.35)
                else:report_and_stop()

        def finish(*_):
            Window.unbind(on_flip=finish)
            try:
                report.parent.mkdir(parents=True,exist_ok=True)
                dashboard=app.root._menu.body
                assert len(dashboard.fixtures.visible_rows)==len(dashboard.data.fixtures)
                result['visible_matchday_fixtures']=len(dashboard.fixtures.visible_rows)
                result['visible_top_scorers']=len(dashboard.scorers.visible_rows)
                app.root.export_to_png(str(report.with_suffix('.png')))
                # Separate static render fixture, not another recorded goal/match.
                g=app.root;g.view='shot';g.state=g.STATE_RESULT;g.shot_context='match'
                g.shot_origin_x=0;g.shot_origin_y=15;g.goalkeeper_x=0
                g.goalkeeper_holding=False;g.goalkeeper_is_diving=False
                g.goalkeeper_dive_progress=0;g.goalkeeper_dive_amount=0
                g.ball.x=1.5;g.ball.y=-.85;g.ball.z=.75;g.ball.active=False
                g.result_text='';g.outcome_registered=True;g.draw()
                Clock.schedule_once(capture_goal,.35)
            except Exception as error:
                result.update(ok=False,error=type(error).__name__+': '+str(error))
                report_and_stop()

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
                # Exercise a completed match using the existing deterministic-safe
                # career path; NPC goals/scorers come from the game's simulation.
                g.view='hub';g.start_career_match()
                assert g.view=='match'
                g._record_player_match_goal();g._finish_career_match()
                assert g.career.matches==1 and g.career.goals==1
                assert g.career.save()
                from career import CareerMode
                restored=CareerMode(autoload=True)
                assert restored.player_name == g.career.player_name
                assert restored.club_name == g.career.club_name
                assert restored.trained_this_week == g.career.trained_this_week
                assert restored.matches == g.career.matches
                assert g.usage.endpoint == '' and not g.usage.enabled
                assert g.ads.backend is None
                assert g.career.save_path.parent == directory
                g.view='hub';g.draw()
                from desktop_dashboard import WindowsDashboard
                assert isinstance(g._menu.body,WindowsDashboard)
                assert len(g._menu.body.data.fixtures)==len(g.career.current_league.clubs)//2
                assert any(row.focus for row in g._menu.body.data.fixtures)
                assert any(row.goals>0 for row in g._menu.body.data.scorers)
                result['matchday_dashboard']=True
                result.update(ok=True,career_reload=True,training=True,free=True,ads_sdk=False,match_completed=True)
                app._close_callback()
                assert g._exit_popup is not None
                popup=g._exit_popup
                popup.dismiss(animation=False)
                assert popup not in Window.children and g._exit_popup is None
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
