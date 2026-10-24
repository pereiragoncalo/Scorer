# SCORER 0.6.12 — compact scoreboard and training before Play

## Changes
- Scoreboard reduced from 360 × 64 dp to 280 × 46 dp, retaining stacked teams,
  clock and goal highlight. Labels now read First half / Second half, with
  Half time / Full time at the breaks. Position remains fixed during chances.
- Training moved immediately left of Play in the match panel. Play is grey and
  disabled until the week's three training shots are completed. A start-match
  guard also enforces the requirement. Next career week requires training again.
- Four secondary navigation buttons remain below. Date moved beside NEXT MATCH.
  The main menu still fits without scrolling, with compact and portrait layouts.
- Interrupted training resumes the same weekly session. Completed shot count
  and goals are saved after each shot; the final reward is applied only once.
  Old reserved sessions without these fields resume from zero recorded shots;
  completed legacy sessions remain complete. Save format stays v2 with optional
  fields training_shots_taken / training_session_goals. Failed writes roll back.
- Match notices stay attached during scene redraws; their canvas is restored
  without removing/re-adding the widget. This avoids reparenting during a touch.
  The reported missed opportunity was not reproduced in the initial test. Its
  original cause is unconfirmed; a touch regression now covers three chances,
  including added time, with scene updates between press and release.

## Files and tests
career.py, main.py, menu_ui.py, buildozer.spec, tests/test_career.py,
ui_tests/test_menus.py, AGENTS.md, README.md and documentation.
33 core/build/security tests and 29 real Kivy tests passed (62). New coverage
includes grey Play gating, training/reload/resume, unlocking after completion,
relocking next week, preserved partial scores, failed writes, duplicate reward
prevention, adjacent buttons and chance touch/navigation without reparenting.
Existing layout, font scaling, pagination, save and half-time tests passed.
Main-menu and chance desktop Kivy captures inspected at 1280×589, density 1.64.
These are not Android device screenshots. APK evidence is in BUILD_LOG.

## Next task
Update the phone without uninstalling. Check the smaller scoreboard, complete
training, confirm Play unlocks and open each chance. Physical validation of
this beta and confirmation of the reported opportunity issue remain pending.
No AAB or store release signing in this step.
