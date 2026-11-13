"""CPU-only reproducible measurements; never claims mobile GPU/frame-rate results."""
import argparse,json,platform,statistics,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from tools.net_lab.scenarios import Replay,PRESETS

def measure():
    rows=[]
    for shape in ('box','veil'):
        for preset in PRESETS:
            r=Replay(shape,preset=preset);samples=[];settled=None
            for _ in range(960):
                start=time.perf_counter();r.one_step();elapsed=time.perf_counter()-start
                if r.hit and r.cloth.active:samples.append(elapsed*1000)
                if r.hit and not r.cloth.active and settled is None:settled=r.tick/120
            ordered=sorted(samples)
            rows.append({'structure':shape,'preset':preset,'particles':len(r.cloth.rest),'links':len(r.cloth.links),
                         'peak_m':r.peak,'peak_time_s':r.peak_time,'settled_s':settled,
                         'physics_step_ms_median':statistics.median(samples),'physics_step_ms_p95':ordered[int(len(ordered)*.95)]})
    return {'platform':platform.system()+' '+platform.machine(),'python':platform.python_version(),
            'measurement':'CPU only on cloud host; no handset or Windows acceptance; physics step includes diagnostic max displacement scan',
            'rows':rows}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();data=measure();a.output.write_text(json.dumps(data,indent=2)+'\n');print(a.output)
