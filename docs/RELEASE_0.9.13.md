# Scorer World 0.9.13 — fairer finishing and richer training/coach screens

World DEBUG QA update; public launch remains 1.0. Save and Exit, install over
World QA, then Load Game. Package and upgrade key are unchanged.

The scoreboard shows team names, score, clock and half without club badges.
Automatic aim stays inside the goal aperture, with ball-radius clearance from
the frame and turf, and visits both flanks and low/high scoring positions.
Hard chances have a 1.18 aim-speed multiplier instead of 1.55 (24% slower), and
retain 78% rather than 60% of the normal shot clock. Division progression remains.
Keeper footwork, acceleration and dive speed are moderately reduced. Both arms
have a constant shoulder-to-glove length throughout the save; the identical
skeleton supplies rendering and collision. High saves use a slightly higher body
jump rather than stretching limbs. Ball trajectory, goal size, opportunity counts
and AI goal accounting are unchanged; no goals/misses are forced.

Weekly practice contains only the player and keeper, with no wall, defenders or
teammates. Three normal finishing shots still save individually, resume after an
interruption, and unlock the match on completion. The training menu adds a
responsive session-plan/progress panel, saved goals/shots, progress bar, energy,
morale and practical timing guidance. Practice is still limited to once per week.

Requested coach meetings show actual recent club goals/appearances and three
paragraphs: situation feedback, a training recommendation, and an encouraging,
demanding or balanced follow-up. All nine UI languages are covered. Meetings
remain limited to drought/key-match triggers; ordinary weeks have no meeting.
Saved portraits, career progress, newspaper and editor paths remain compatible.

Validation: 340 core and 153 native Kivy tests. Added coverage samples 28,800 aim
positions, 126 save poses with extreme targets, 50 training origins, scoreboard
badge exclusion, persisted training progress and all three feedback contexts in
nine languages. Existing translated/small-window coach access remains covered.
An initial run exposed a new training-field typo and old timing/reach assumptions;
these were corrected before the final full runs and final APK build.

Seeded physical reference runs used 25 shots per tier/strategy/chance type,
1,000 per version. For hard placed shots, conversion rose from 72% to 80% in
tier 5, 56% to 72% in tier 2 and 52% to 64% in tier 1. These are ideal exact target
shots bypassing aim/timers. Shot origins can differ between versions as random
draws change, so these are reference outcomes, not an isolated effect estimate,
human performance or device measurements. Full
current outcomes are in docs/data/difficulty_0.9.13.json. Difficulty needs owner
feedback on a real handset.

Desktop Kivy previews show the actual Portuguese training and coach menus.
APK checks cover package/API, existing QA certificate, 16 KB alignment, exact
compiled gameplay source, competition persistence and ad-free payload. Physical
Android validation, production signing and Google Play submission are not done.
