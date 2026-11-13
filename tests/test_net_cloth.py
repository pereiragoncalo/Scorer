import json,math,tempfile,time,unittest
from dataclasses import replace,asdict
from pathlib import Path
from net_cloth import NetConfig,NetGeometry,NetCloth
from tools.net_lab.scenarios import Replay,PRESETS

class ClothTests(unittest.TestCase):
 def test_seven_presets_finite_pinned_recover_and_stop_for_both_shapes(self):
  for structure in ('box','veil'):
   for preset in PRESETS:
    with self.subTest(structure=structure,preset=preset):
     replay=Replay(structure,preset=preset)
     for _ in range(1080):replay.advance(1/120)
     c=replay.cloth
     self.assertGreater(replay.peak,.025);self.assertFalse(c.active);self.assertEqual(c.displacement,0.)
     self.assertTrue(all(math.isfinite(v) for p in c.positions for v in p))
     self.assertTrue(all(c.positions[i]==c.rest[i] for i,fixed in enumerate(c.pinned) if fixed))
     generation=c.generation;self.assertEqual(c.advance(1/60),0);self.assertEqual(c.generation,generation)
 def test_strength_near_far_symmetry_and_peak_after_contact(self):
  peaks=[]
  for name in ('Near Post Weak','Near Post Medium','Near Post Strong','Far Post Strong'):
   r=Replay(preset=name)
   for _ in range(180):r.one_step()
   peaks.append(r.peak);self.assertGreater(r.peak_time,.30)
  self.assertLess(peaks[0],peaks[1]);self.assertLess(peaks[1],peaks[2]);self.assertAlmostEqual(peaks[2],peaks[3],delta=.03)
  self.assertGreater(peaks[2],.5);self.assertLess(peaks[2],1.7)
 def test_playback_rates_are_same_trajectory_and_frame_rates_repeat(self):
  baseline=None
  for fps in (30,60,120):
   for speed in (1.,.5,.25):
    r=Replay();r.playback=speed
    for _ in range(round(1.2*fps/speed)):r.advance(1/fps)
    state=(r.tick,r.cloth.positions,r.ball)
    if baseline is None:baseline=state
    self.assertEqual(state,baseline)
 def test_seams_are_welded_and_sag_is_rest_geometry(self):
  for shape in ('box','veil'):
   c=NetCloth(NetGeometry(shape));tight=NetCloth(NetGeometry(shape),replace(NetConfig(),net_slack=0))
   self.assertNotEqual(c.rest,tight.rest)
   for side,edge in (('left',0),('right',-1)):
    back=c.grids['back'][2]
    side_ids={i for row in c.grids[side][2] for i in row}
    self.assertTrue(all(row[edge] in side_ids for row in back))
 def test_config_roundtrip_and_invalid_inputs(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'config.json';r=Replay('veil',preset='Top Corner');r.save(path);other=Replay.load(path)
   for _ in range(120):r.one_step();other.one_step()
   self.assertEqual(r.cloth.positions,other.cloth.positions)
   data=json.loads(path.read_text());data['parameters']['net_damping']=float('nan');path.write_text(json.dumps(data))
   with self.assertRaises(ValueError):Replay.load(path)
  for kwargs in ({'net_damping':-1},{'net_max_stretch':99},{'net_impact_scale':float('inf')}):
   with self.assertRaises(ValueError):NetConfig(**kwargs)
  c=NetCloth()
  with self.assertRaises(ValueError):c.impact('back',(0,0,1),(float('nan'),0,0))
 def test_repeated_strong_impacts_are_bounded(self):
  c=NetCloth();p=c.geometry.point('left',.25,.5)
  for tick in range(720):
   if tick%36==0:c.impact('left',p,(-50,-10,4))
   c.advance(c.STEP)
   self.assertLess(c.displacement,2.)
  for _ in range(1200):c.advance(c.STEP)
  self.assertFalse(c.active)
