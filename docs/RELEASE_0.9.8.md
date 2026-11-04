# Scorer World 0.9.8 — decisive match moments

World QA update; the public launch remains 1.0. Save and Exit, install over the
existing World QA app, then Load Game. Existing careers receive the feature;
no new career or reset is necessary.

## What changes

Before selected chances, the game explains the actual stakes: a late equaliser,
a late chance to lead, a cup final, a promotion/relegation playoff, a local derby
or a close survival run-in. The ordinary Play Chance button starts the same
physical shot as before. Context is available in all nine UI languages.

At most one existing opportunity per match can move into the final minutes.
This happens in 45% of ordinary matches and 75% of matches with recognised stakes,
unless an opportunity is already late. There is no extra chance. The independent
seeded timing draw does not consume career RNG, inspect future goals, change
AI goals/timing, grant clear chances or change shot physics/difficulty.

The late score message uses the live scoreboard at the pause, with the player's
home/away orientation and a displayed clock that excludes first-half added time.
It never promises the eventual winner. Two-legged ties retain the playoff/final
context instead of mistaking a level leg score for a level aggregate.

One featured chance per match is recorded with its kind, minute and physical
outcome. The final notice and Fixtures history display it; it survives reload.
There are no extra goals, morale rewards, trophy awards or scripted outcomes.

## Context boundaries

Final means the actual fixture stage `Final`, not a semifinal. Playoff context
covers upper-division clubs defending their place as well as promotion hopefuls.
Thirteen curated rivalry pairs use immutable club UIDs, so imported names cannot
create or erase a derby. This is partial rivalry coverage, not a global catalogue.

Survival context uses the current game's direct relegation boundary, within the
last five scheduled league rounds, for a player near that boundary and within
three points of the other side. It says every point matters; it does not claim
that scoring guarantees safety. Split schedules and playoff rules remain as in
0.9.7; this update adds no newly verified national formats.

## Validation

Core simulation/localisation and native Kivy integration tests cover chance
conservation, unchanged AI RNG/goals/difficulty index, live home/away scores,
second-half timing, duplicate goal protection, future events, aggregate wording,
UID-based derbies, survival context, history reload, all nine languages and a
320×240 scrollable notice with a reachable action. The retained notice refreshes
its text when the UI language changes.

The APK is built and statically checked for API36/arm64, 16KB ELF/ZIP alignment,
existing DEBUG upgrade certificate, exact compiled source, competition/save
smokes, ad-free payload and publishing safeguards. It has not been tested on a
physical Android device, production signed or submitted to Google Play.
