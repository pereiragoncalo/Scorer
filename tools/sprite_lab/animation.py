"""Standalone presentation clock. Never imports or changes Scorer's gameplay."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

def load_manifest():
    return json.loads((ROOT / 'assets/sprites/manifest.json').read_text())

class Animation:
    def __init__(self, character, state):
        self.character = character
        self.state = state
        self.frame = 0
        self.elapsed = 0.0
        self.speed = 1.0
        self.paused = False
        self.repeat = True  # Viewer replay; production clips retain their loop flag.
        self.flipped = False

    @property
    def clip(self):
        return self.character['animations'][self.state]

    def select(self, state):
        if state not in self.character['animations']:
            raise ValueError(state)
        self.state, self.frame, self.elapsed = state, 0, 0.0

    def update(self, dt):
        if self.paused:
            return
        self.elapsed += max(0.0, dt) * self.speed * self.clip['fps']
        steps = int(self.elapsed + 1e-9)
        self.elapsed -= steps
        if self.repeat or self.clip['loop']:
            self.frame = (self.frame + steps) % self.clip['frames']
        else:
            self.frame = min(self.frame + steps, self.clip['frames'] - 1)

    def step(self, delta=1):
        self.paused, self.elapsed = True, 0.0
        self.frame = (self.frame + delta) % self.clip['frames']

    def event(self, event, direction=1):
        """Future presentation adapter contract; not connected to the game."""
        state = 'DIVE_LEFT' if event == 'DIVE' and direction < 0 else 'DIVE_RIGHT' if event == 'DIVE' else event
        self.select(state)
