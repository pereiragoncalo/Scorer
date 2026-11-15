import tempfile,unittest,wave
from pathlib import Path
from goal_audio import generate
class GoalAudio(unittest.TestCase):
 def test_waveform_is_complete_and_cached(self):
  with tempfile.TemporaryDirectory() as root:
   path=Path(root)/'goal.wav';generate(path);before=path.read_bytes()
   with wave.open(str(path)) as w:
    self.assertEqual((w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes()),(1,2,22050,51817))
   generate(path);self.assertEqual(path.read_bytes(),before)
   self.assertEqual(list(Path(root).iterdir()),[path])
