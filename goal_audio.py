"""Prepare the original crowd waveform before gameplay, never on a goal frame."""
import math,random,struct,wave,weakref,tempfile,os
from pathlib import Path
from threading import Thread
from career import clamp

def generate(sound_path):
    sound_path=Path(sound_path)
    if sound_path.exists():return
    sample_rate = 22050
    duration = 2.35
    count = int(sample_rate * duration)
    rng = random.Random(92831)
    samples: list[int] = []
    smooth = 0.0
    for index in range(count):
        t = index / sample_rate
        raw = rng.uniform(-1.0, 1.0)
        smooth = smooth * 0.86 + raw * 0.14
        voices = (
            0.34 * math.sin(2.0 * math.pi * 176.0 * t + 0.3)
            + 0.25 * math.sin(2.0 * math.pi * 223.0 * t + 1.7)
            + 0.18 * math.sin(2.0 * math.pi * 287.0 * t + 2.4)
        )
        attack = min(1.0, t / 0.11)
        decay = max(0.0, 1.0 - max(0.0, t - 0.55) / 2.0)
        pulse = 0.82 + 0.18 * math.sin(2.0 * math.pi * 3.2 * t)
        value = (smooth * 0.78 + voices) * attack * decay * pulse
        samples.append(int(clamp(value, -1.0, 1.0) * 14500))
    fd,temporary=tempfile.mkstemp(prefix='.scorer-crowd-',suffix='.wav',dir=sound_path.parent)
    os.close(fd)
    try:
        with wave.open(temporary, "wb") as sound_file:
            sound_file.setnchannels(1)
            sound_file.setsampwidth(2)
            sound_file.setframerate(sample_rate)
            sound_file.writeframes(struct.pack("<" + "h" * len(samples), *samples))
        os.replace(temporary,sound_path)
    finally:
        Path(temporary).unlink(missing_ok=True)

def preload(game):
    from kivy.clock import Clock
    ref=weakref.ref(game)
    path=game.career.save_path.parent/'striker_goal_crowd.wav'
    def ready(_):
        owner=ref()
        if owner is None:return
        try:
            from kivy.core.audio import SoundLoader
            owner._goal_crowd_sound=SoundLoader.load(str(path))
        except Exception:owner._goal_crowd_sound=None
    def work():
        try:generate(path)
        except Exception:return
        Clock.schedule_once(ready,0)
    Thread(target=work,name='scorer-goal-audio',daemon=True).start()
