"""Headless real match/shot physics calibration with an instantaneous aim bot.

Runs actual weekly training, fixture planning, goal events, physical shots and
career progression in temporary saves. Club fixtures only (cups/call-ups off)
to compare with domestic league data. This is not an Android/human test.
"""
import argparse
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
from kivy.core.window import Window


def experiment(matches=100, strategy='uniform'):
    totals=personal=chances=high_scores=draws=nil_nil=0
    old_state=random.getstate()
    with tempfile.TemporaryDirectory() as root, patch.dict(os.environ, STRIKER_SAVE_DIR=root):
        random.seed(61317)
        game=StrikerGame();Clock.unschedule(game.update);game.draw=lambda:None
        game.size=(960,540)
        c=game.career;c.accept_starting_offer(c.offers[0]);aim=random.Random(1729)
        try:
            with patch.object(game,'_play_goal_crowd_sound'), patch.object(game,'_play_ai_goal_sound'), patch.object(game,'_play_chance_sound'):
                for _ in range(matches):
                    c.called_up=False;c.cup_active=False
                    c.begin_training()
                    for shot in range(3):
                        c.record_training_shot(True)
                    c.complete_training(3)
                    game.view='hub';game.start_career_match()
                    chances+=len(game.match_chance_minutes)
                    iterations=0
                    while not game.match_finished:
                        iterations+=1
                        if iterations>100:
                            raise RuntimeError('Match did not finish')
                        if game.match_halftime:
                            game._resume_second_half()
                        elif game.awaiting_chance:
                            game._begin_pending_chance();game.power=0.85
                            x,z=((3.45 if aim.random()<0.5 else -3.45),2.25) if strategy=='corners' else (aim.uniform(-3.25,3.25),aim.uniform(0.25,2.20))
                            game.shoot(x,z)
                            for step in range(int(30/PHYSICS_STEP)):
                                game.elapsed+=PHYSICS_STEP;game.state_age+=PHYSICS_STEP
                                game._update_goalkeeper_shot(PHYSICS_STEP)
                                game._update_ball(PHYSICS_STEP)
                                if game.outcome_registered:
                                    break
                            if not game.outcome_registered:
                                raise RuntimeError('Unresolved physical shot; not counted as a forced miss')
                            game._advance_after_shot()
                        else:
                            game._update_career_match(100)
                    a,b=game.match_home_score,game.match_away_score
                    totals+=a+b;personal+=game.match_player_goals
                    high_scores+=a+b>=5;draws+=a==b;nil_nil+=a==b==0
        finally:
            random.setstate(old_state)
            Window.unbind(on_key_down=game._on_key_down)
    return dict(matches=matches,strategy=strategy,goals_per_match=totals/matches,
        personal_goals=personal,personal_chances=chances,conversion=personal/max(1,chances),
        five_plus_rate=high_scores/matches,draw_rate=draws/matches,nil_nil_rate=nil_nil/matches)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--matches',type=int,default=100)
    parser.add_argument('--strategy',choices=('uniform','corners'),default='uniform')
    args=parser.parse_args()
    if not 1<=args.matches<=1000:
        parser.error('--matches must be between 1 and 1000')
    print(json.dumps(experiment(args.matches,args.strategy),sort_keys=True))
