# Scorer World0.9.32 — weekly locker-room team talks

The coach now addresses the squad once each career week, including the first
week. The talk opens before training, normally after the previous match's
newspaper when the career advances into the next week. Additional club/cup/
international matches in the same week keep the chosen focus and do not request
another talk. A new season or club starts a new coach briefing.

The one-screen locker-room presentation combines collective feedback from actual
club results (including shootouts), named individual feedback from recent goals,
key matches or drought, and the coach's established personality. It uses a new
original locker-room photo and the existing ten saved coach faces as cropped
avatars. Smaller screens use complete concise feedback sentences. No scroll or
second page; the footer retains two focus options, Help and the finish action.
New/updated guidance is translated into all nine languages.

Exactly two weekly training focuses are offered. The player's explicit selection
is required to enable Finish Team Talk. The offers are deterministic without
consuming gameplay RNG. The choice, acknowledgement and post-match queue save
atomically and all roll back on failure. No morale/trust/energy/XP reward is given
for attending or repeating the completion callback. The focus stays fixed for
all sessions in that week. Training retains progress and stats but no focus
selector; stale training-focus actions cannot change the choice. Focus guidance
is in the team-talk Help. Gameplay has no Help button; its original scoreboard
available width is restored. Help remains on the other normal screens.

Existing careers retain progress and skills. Old coach acknowledgements without
a weekly focus require the new talk. An unfinished old drill keeps its original
focus and XP until completion; the new choice applies to following sessions.
A new week clears a stale development session so its old focus/reward flag cannot
override the next choice. Training still requires three persisted shots before
every match. Existing shot physics, collisions, chance caps, club kits, news,
continental competitions, standings, editor and online behaviour are unchanged.

Validation:399 core cases completed (3 skipped), all207 native Kivy cases passed,
including11 core coach regressions and5 focused native coach tests.231 responsive
cases across11 phone/density/font profiles and Portuguese/German/Japanese had zero
findings; all33 coach cases were checked again after the final font adjustment.
Team talk, selected option and training screenshots were visually inspected.
Legacy conditional-meeting/focus-picker expectations and unrelated fixture setup
were updated for the weekly contract; unrelated root WIP is excluded from staging.

Actual World DEBUG QA APK: same package/upgrade certificate, code1026932,
API36/min26, arm64, ZIP16KB and118 aligned ELF files.208 sprites/30 sheets remain,
and exact compiled main/coach/progression/menu/help/standings sources plus locker-
room PNG match staging. Actual APK weekly offers, saved choice, same-week lock,
next-week gate, focused XP, old competition and save/import checks pass. Physical
Android playtest remains pending. No Play submission or production1.0 change.

[Download APK](https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.32/Scorer-World-0.9.32.apk).
