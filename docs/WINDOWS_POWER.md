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

Validation: core/security161 pass; actual Kivy93 pass (including6 focused profile/render checks) including unchanged
Android profile and crowd call checks; native Windows run40743617913 PASS:6 staging checks, frozen career/training/match/save-reload/close and nonblank hub/goal/empty-training FBO renders.
Files: main.py, desktop_launcher.py, tools/windows/verify_smoke.py,
ui_tests/test_goal_geometry.py. No new dependencies, network uploads or secrets.
Next: Windows human mouse/keyboard match/training test and save/reload.

Unsigned Windows x64 EXE: 41566939bytes. SHA256 `e515818e052573f7f0c76f271a3246085ba19ae93ed07c51ad9c18209c98e529`.
[Download win.4](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/windows-beta-0.6.39-4/Scorer-Free.exe).
Static training capture reuses the test result state (SHOT4/3), not a playable fourth training attempt. No claim of full human match validation.
