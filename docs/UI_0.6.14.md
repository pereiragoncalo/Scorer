# SCORER 0.6.14 — attached shot timer and player initials

## Changes
- TIME TO SHOOT is now a compact 22 dp strip directly beneath the scoreboard,
  sharing its left edge and width. A thin progress bar retains urgency feedback.
  Shot time, difficulty, score layout and match clock are unchanged.
- Player names automatically uppercase the first letter of each space-separated
  component: gonçalo pereira → Gonçalo Pereira; joão da silva → João Da Silva.
  Internal spelling is retained (Sean McDonald stays Sean McDonald).
- Applies to new profiles, profile edits and loaded careers. The scorer key
  migrates together with the player name, retaining goals and other scorers.
  If an old save already has a different scorer with the exact formatted name,
  leave both records intact rather than overwrite either; profile editing can
  resolve that exceptional ambiguity. Failed rename saves roll back as before.

## Files and tests
career.py, main.py, buildozer.spec, tests/test_career.py, ui_tests/test_menus.py,
AGENTS.md, README.md and documentation. No save format or baseline change.
36 core/build/security tests + 31 Kivy tests passed (67). New coverage includes
accented multi-part initials, internal capitals, legacy scorer migration,
collision preservation and failed writes. Existing real Kivy geometry test
now checks identical timer/scoreboard edges, direct attachment across three
screen densities and an unchanged countdown value.

A real Kivy window capture of the attached timer was inspected at 1280×589,
density 1.64. This is not an Android screenshot. APK build/static evidence is
in BUILD_LOG. Next: update without uninstalling and check timer attachment
and the player name in the phone's main menu/scorers. Physical validation of
this beta remains pending. No AAB or store release signing in this step.
