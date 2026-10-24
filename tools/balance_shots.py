"""Seeded physical shot experiment; no score quotas or forced outcomes.

Run from the repo with the development Kivy interpreter, for example:
SDL_VIDEODRIVER=offscreen python tools/balance_shots.py --samples 240
The legacy standard generator is retained for comparison. This is not a
human touch/device test or a prediction of season scoring rates.
"""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import random
import sys
import tempfile
from unittest.mock import patch

os.environ.setdefault('KIVY_NO_ARGS', '1')
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import StrikerGame, PHYSICS_STEP
from kivy.clock import Clock


def experiment(samples=240, max_seconds=15, strategy="uniform"):
    results = {}
    previous_random = random.getstate()
    with tempfile.TemporaryDirectory() as root, patch.dict(os.environ, STRIKER_SAVE_DIR=root):
        game = StrikerGame()
        game.size = (960, 540)
        Clock.unschedule(game.update)
        game.shot_context, game.view = 'match', 'shot'
        try:
            for profile in ('standard', 'easy', 'hard', 'training'):
                game.shot_context = 'training' if profile == 'training' else 'match'
                outcomes = Counter()
                for seed in range(samples):
                    random.seed(39000 + seed)
                    game.career.rng.seed(67000 + seed)
                    game.current_chance_difficulty = profile
                    game.elapsed = 0
                    game._prepare_next_shot()
                    game.power = 0.85
                    target = random.Random(98000 + seed)
                    x, z = ((3.45 if seed % 2 else -3.45), 2.25) if strategy == "corners" else (target.uniform(-3.25, 3.25), target.uniform(0.25, 2.20))
                    with patch.object(game, '_play_goal_crowd_sound'):
                        game.shoot(x, z)
                        for _ in range(int(max_seconds / PHYSICS_STEP)):
                            game.elapsed += PHYSICS_STEP
                            game.state_age += PHYSICS_STEP
                            game._update_goalkeeper_shot(PHYSICS_STEP)
                            game._update_ball(PHYSICS_STEP)
                            if game.outcome_registered:
                                break
                    outcomes[game.result_text or 'UNRESOLVED'] += 1
                results[profile] = dict(outcomes)
        finally:
            random.setstate(previous_random)
            from kivy.core.window import Window
            Window.unbind(on_key_down=game._on_key_down)
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--samples', type=int, default=240)
    parser.add_argument('--strategy', choices=('uniform', 'corners'), default='uniform')
    args = parser.parse_args()
    if not 1 <= args.samples <= 10000:
        parser.error('--samples must be between 1 and 10000')
    print(json.dumps(experiment(args.samples, strategy=args.strategy), sort_keys=True))
