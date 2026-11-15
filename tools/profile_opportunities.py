"""Local Kivy CPU profile; timings include cProfile overhead, not handset FPS."""
import sys,time,cProfile,pstats,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path[:0]=[str(ROOT),str(ROOT/'ui_tests')]
if os.environ.get('SCORER_PROFILE_BASELINE'):sys.path.insert(0,os.environ['SCORER_PROFILE_BASELINE'])
from kivy.clock import Clock
from test_menus import isolated_game
from goal_nets import ROUNDED_STYLE
with isolated_game() as g:
 Clock.unschedule(g.update);g.size=(1280,720);g.view='shot';g.shot_context='training';g.training_shots_left=3;g._goal_net_style_override=ROUNDED_STYLE
 g._start_opportunity('long_cross',35);g.draw()
 p=cProfile.Profile();p.enable();times=[]
 for _ in range(30):
  t=time.perf_counter();g.update(1/60);times.append((time.perf_counter()-t)*1000)
 p.disable();print('BUILDUP_MS',sum(times)/len(times),max(times));pstats.Stats(p).sort_stats('cumtime').print_stats(12)
 g.ball.x=0;g.ball.y=0;g.ball.z=1;g.ball.vx=0;g.ball.vy=-22;g.ball.vz=0;g.outcome_registered=False
 t=time.perf_counter();g._register_goal((0,0,1),0);print('GOAL_START_MS',(time.perf_counter()-t)*1000)
 g.state=g.STATE_RESULT;p=cProfile.Profile();p.enable();times=[]
 for _ in range(40):
  t=time.perf_counter();g.update(1/60);times.append((time.perf_counter()-t)*1000)
 p.disable();print('GOAL_FRAME_MS',sum(times)/len(times),max(times));pstats.Stats(p).sort_stats('cumtime').print_stats(18)
