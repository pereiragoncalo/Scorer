# SCORER 0.6.11 — scoreboard and half-time

## Changes
- A shared compact scoreboard at the top left: home and away on separate rows,
  badges, score per row and clock on the right. Identical geometry during match
  simulation, chance notices and interactive shots. No bottom match-time bar.
- A one-second local green pulse for every goal, home or away. Player goals
  update the score immediately when the ball crosses the line, with a per-shot
  guard preventing the Continue action from counting the goal twice.
- First-half added time (1–4 minutes) and HALF-TIME pause. SECOND HALF resumes
  the clock at 45:00; second-half added time (existing 1–8 minutes) follows 90.
  The internal timeline includes both periods while the displayed clock
  subtracts first-half added time in the second half. Clock displays seconds.
- The event scheduler stops at the next chance or half boundary before
  processing goals. This also fixes future goals being counted before an
  earlier chance when an update crosses multiple event times.
- Match notices and the shot countdown sit below the scoreboard. Existing
  English text, career, weekly training, physics and save format retained.

## Files
main.py, menu_ui.py, buildozer.spec, ui_tests/test_menus.py, AGENTS.md, README.md
and documentation. Immutable baseline and career.py unchanged.

## Validation and next task
Test results and APK evidence are recorded in BUILD_LOG. Coverage includes
half-time/added-time boundaries, clock resumption, events at a half boundary,
home/away goal highlights, immediate player goals without duplicate counts,
scoreboard draw geometry across densities, and countdown/notice separation.
Screenshots from a real Kivy window are desktop captures, not Android captures.
Next: update the phone, score/concede a goal, play a chance and continue from
half-time. Physical validation of this beta remains pending; no AAB or store
release signing in this step.
