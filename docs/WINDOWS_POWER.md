# Windows Free 0.6.39-win.4

Windows only: goalkeeper pose, reach/collision volumes and rendered thickness
reduced14%; shot flight duration divided by1.22 (22%higher horizontal velocity)
with gravity recomputed to retain aim destination. Includes headers and ordinary
shots, normal training/match code. Original Android scale, speed/clamps and crowd
remain exact under the default profile. No Android APK rebuilt. Shared constants,
career schema, goal dimensions, aim dispersion and NPC results unchanged.

Windows training hides only crowd mesh draws; real stand geometry remains.
Match crowds return automatically without invalidating caches. Sponsor boards stay.

Paired80-seed hard-shot bot calibration: original18goals/37saves/25misses;
previous Windows26goals/34saves/20misses; current37goals/19saves/24misses.
All resolve through physical code. Bot corners/instant aim are not human rates;
owner should play a full match before accepting difficulty. No automatic goals.

Validation: core/security161 pass; focused actual Kivy6 pass including unchanged
Android profile and crowd call checks; native build/frozen render evidence pending.
Files: main.py, desktop_launcher.py, tools/windows/verify_smoke.py,
ui_tests/test_goal_geometry.py. No new dependencies, network uploads or secrets.
Next: Windows human mouse/keyboard match/training test and save/reload.
