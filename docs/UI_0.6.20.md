# SCORER 0.6.20 — practice, confidence and match presentation

## Changes

- Practice now uses 13–17 m angled shots, moderate physical launch dispersion
  (0.60 m horizontal / 0.40 m vertical before condition/power), and the match
  ball-speed model (18 + power × 8 m/s). It no longer uses near-perfect aim and
  a faster ball than matches. Three shots, weekly reservation, resumption and
  rewards are unchanged. No real-world conversion claim is made for training.
- Hard match shots start at 15.5–20 m, 4–7.5 m lateral offset. Dispersion reduces
  from 0.95/0.65 to 0.78/0.53 m; keeper reaction becomes 0.18–0.27 s, lateral
  speed 3.0 m/s, dive speed 5.2. Clear chances and opponent quantity caps stay.
- Expected hard contribution is 0.20 rather than 0.18 when reserving the player
  share from teammate goals. The 2.61 goal budget and physical outcomes stay.
- Morale gains 1.20 per goal and loses only 0.25 per missed chance (was ±0.85),
  bounded to 0–20. Stamina rules are unchanged.
- Each club has a deterministic fictional full-name squad; the heavily weighted
  striker is no longer called Silva in every club. Recognised old generated
  scorer keys migrate on load, merging matching entries without losing goals;
  player/custom names and past fixtures remain intact. Stable local roster RNG
  does not consume simulation randomness.
- Confirmed central body saves while standing secure the ball, bring the hands
  together and pitch the goalkeeper forward over 0.65 s. The ball stays attached
  and the save counts once. Diving/high parries remain physical and can rebound.
- Two visible end-line corners gain 1.5 m poles, triangular flags and corner arcs,
  projected in pitch space. The game renders a half pitch, not four full corners.
- Compact fixed broadcast scoreboard: dark team rows, separate score column,
  clock block, accent strip and subtle shadow, replacing the outer wire outline.
  Goal pulses, half labels, attached countdown and position remain.

## Evidence

49 core/build/security tests and 38 real Kivy tests pass (87 total). Added tests
cover morale bounds, stable/distinct squad names, save migration preserving
scorer totals, and single-counted possession/fall/reset. Existing weekly-session,
match/touch/half-time, schedule, saves and layout regression tests pass. Syntax
and git whitespace checks pass; immutable baseline hash test passes.

Seeded physical experiments, 240 attempts/profile, same uniforms before/after:

| Profile | 0.6.19 | 0.6.20 |
| --- | ---: | ---: |
| Training, uniform aim | 131/240 (54.6%) | 75/240 (31.3%) |
| Hard match, uniform aim | 44/240 (18.3%) | 49/240 (20.4%) |
| Clear match, uniform aim | 122/240 (50.8%) | 122/240 (50.8%) |

Final corner-aim bot: hard 97/240 (40.4%), training 108/240 (45.0%). This bot
instantly picks a goal corner; these are experiments, not human Android results
or population estimates. The previous documented hard corner sample was 72/240.
100 complete playable league matches with the uniform instant-aim bot, maximum
training goals, produced 2.46 total goals/match, 59 personal goals from 224
chances (26.3%). This small artificial sample is not proof of real-world season
accuracy. See docs/data/balance_0.6.20.json and the existing realism sources.

Commands: unittest discovery for tests/ and ui_tests/; tools/balance_shots.py
--samples 240 --strategy uniform/corners; tools/calibrate_playable.py --matches
100 --strategy uniform. Kivy ran SDL offscreen with real GL. Actual desktop
screenshots inspected: /workspace/striker-runtime/scorer-0620-scoreboard0001.png
and scorer-0620-catch0001.png. Physical phone confirmation is pending.

## Artifact and next task

Actual debug APK compiled, package com.clemir.striker, versionCode 1026620,
min API 26, target API 36, arm64-v8a. Signature v2 uses the same existing debug
certificate; ZIP 16 KB alignment and all 118 AArch64 ELF checks pass. No Android
permissions, saves or private signing keys in the payload. Not a release AAB.

APK: 30,215,905 bytes. SHA256:
`d2d938c1f8331a81db65f037b652a65c1632b8a4ad8282932a67bd4a1f008114`.

Next: install as an update, check training difficulty versus hard match shots,
standing catch/fall, scoreboard legibility/goal pulse, flags and resumed career
on a real phone. No uninstallation or new career is needed for these changes.
