# SCORER 0.6.13 — finishing balance and menu logo

## Changes
- Personal highlights now range from zero to three per match, varying with
  energy and morale. Previously up to five were possible. A match has a 60%
  chance of allocating exactly one clear opportunity; otherwise all are hard.
  Its index is chosen once at kick-off, so there can never be two clear chances.
- Clear chances retain nearby kicks, penalties and headers. Hard chances are
  kicks or free kicks from 16.5–21 m and 4.5–8 m off-centre, with four physical
  defenders / a free-kick wall. Camera-edge cases mirror the same shot angle
  to the visible side, retaining distance and defensive pressure. The pressured keeper reacts in 0.07–0.13 s,
  reads the ball more accurately and moves/dives faster. Decision time is 60%
  of the competitive profile (minimum 2.7 s), with a faster automatic aim.
- Touch aiming still works. Goals remain determined by ball/keeper/defender
  physics; there is no automatic miss, score ceiling or rival-stat inflation.
  Existing career goals and progress are retained. Training is unchanged.
- New transparent ivory/emerald SCORER logo generated from the existing S/ball
  icon for the main hub and New/Load entry screen. No by clemir on those menus.
  Original app icon and splash credit remain unchanged.

## Validation
34 core/build/security tests and 31 Kivy tests passed (65). New tests cover
chance-count bounds/condition, sixty seeded match allocations, maximum one
clear chance, hard positions/defenders/timer, retained shot types, viewport,
keeper response, unchanged training and a hub without an author credit.

A reproducible experiment runs actual ball/keeper/defender physics with 240
seeded shots per profile (720 total), power 0.85 and the same target samples:

| Profile | Goals | Saves | Misses | Conversion |
| --- | ---: | ---: | ---: | ---: |
| Previous generator | 109 | 100 | 31 | 45.4% |
| New clear chance | 177 | 63 | 0 | 73.8% |
| New hard chance | 62 | 104 | 74 | 25.8% |

Reproduce using the development Kivy interpreter:
`SDL_VIDEODRIVER=offscreen python tools/balance_shots.py --samples 240`.
The experiment uses isolated temporary saves and caps each shot at 15 simulated
seconds; all samples resolved. It tests physical shots with fixed target
sampling, not human touch skill, season standings or Android performance.
Physical device balancing still needs feedback from real matches.

## Files and next task
career.py, main.py, menu_ui.py, assets/menu_logo.png, buildozer.spec,
tests/test_career.py, ui_tests/test_menus.py, tools/balance_shots.py, AGENTS.md,
README.md and documentation. Baseline unchanged. APK evidence is in BUILD_LOG.
Desktop Kivy menu and hard free-kick captures inspected; not Android captures.
Next: update without uninstalling, play several matches and compare conversion
of hard chances. No AAB or store release signing in this step.
