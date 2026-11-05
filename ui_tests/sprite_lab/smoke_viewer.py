"""Real Kivy/SDL2 smoke; run standalone, optionally SDL_VIDEODRIVER=offscreen."""
import sys,json,time,resource
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from tools.sprite_viewer import SpriteLab
from tools.sprite_lab.animation import ROOT
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
OUT=ROOT/'docs/sprite_lab';OUT.mkdir(exist_ok=True)
EventLoop.ensure_window();lab=SpriteLab();Window.add_widget(lab)

def settle():
    for _ in range(3):Clock.tick();EventLoop.idle()

settle()
checks=0
for p in lab.panels:
    for view in p.animation.character['views']:
        p.view=view
        for state,clip in p.animation.character['animations'].items():
            p.select(state)
            for frame in range(clip['frames']):
                p.animation.frame=frame
                texture,uv=lab.cache.frame(p.animation.character,clip,view,frame,p.colours)
                assert texture.mag_filter==texture.min_filter=='nearest'
                # Compare the source atlas crop with the individual PNG bytes.
                source=CoreImage(str(ROOT/clip['sheets'][view]['path'])).texture
                individual=CoreImage(str(ROOT/clip['individuals'][view][frame])).texture
                w,h=p.animation.character['canvas'];col=frame%clip['sheets'][view]['columns'];row=frame//clip['sheets'][view]['columns']
                # PNG .pixels is top-down for this Kivy SDL2 loader.
                source_pixels=bytes(source.pixels)
                crop=b''.join(source_pixels[((row*h+y)*source.width+col*w)*4:((row*h+y)*source.width+col*w+w)*4] for y in range(h))
                assert crop==individual.pixels,(state,frame)
                p.stage.redraw();checks+=1
            for mode in ('Frames','Sheet','Animation'):
                p.mode=mode;p.stage.redraw()
            p.flip();p.stage.redraw();p.flip()
lab.pause();assert all(p.animation.paused for p in lab.panels)
lab.step(1);lab.step(-1);lab.speed(None,.5);lab.change_scale(None,'4')
for size in [(960,640),(1280,800),(1440,900)]:
    Window.size=size;settle()
    for p in lab.panels:
        assert p.stage.height>=130
        assert p.stage.x>=0 and p.stage.right<=Window.width+1
        assert p.stage.y>=0 and p.stage.top<=Window.height
lab.change_scale(None,'5')
for p,state in zip(lab.panels,('SHOOT','DIVE_RIGHT')):
    p.view=p.animation.character['views'][0];p.select(state);p.animation.frame=4;p.animation.paused=True
settle();lab.tick(0)
lab.export_to_png(str(OUT/'viewer.png'))
for p in lab.panels:p.stage.export_to_png(str(OUT/f'{p.role}-stage.png'))
# Warm current sheets; steady-state playback should create no new textures.
for p in lab.panels:p.animation.paused=False
lab.tick(.016);before=lab.cache.allocations;t=time.perf_counter()
for _ in range(2000):lab.tick(1/60)
seconds=time.perf_counter()-t
assert lab.cache.allocations==before
assert len(lab.cache.entries)<=lab.cache.limit
assert 'main' not in sys.modules and 'career' not in sys.modules
render_start=time.perf_counter()
for _ in range(120):lab.tick(1/60);EventLoop.idle()
render_seconds=time.perf_counter()-render_start
result=dict(rendered_frames=120,rendered_seconds=round(render_seconds,4),kivy='2.3.1',backend='SDL2 offscreen / Mesa llvmpipe',frames_checked=checks,simultaneous_characters=2,layouts=[[960,640],[1280,800],[1440,900]],steady_state_updates=2000,update_seconds=round(seconds,4),mean_update_ms=round(seconds/2,4),texture_allocations_during_updates=lab.cache.allocations-before,cached_textures=len(lab.cache.entries),max_cached_textures=lab.cache.limit,source_pixel_bytes=sum(len(v[1]) for v in lab.cache.sources.values()),process_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,android_device_tested=False)
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
lab.tick_event.cancel()
