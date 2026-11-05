# Scorer World 0.9.20 — goals, skills and coach trust

World DEBUG QA upgrade. Install over the existing World QA and choose Load Game.
The package, upgrade certificate, careers, club IDs, names, trophies and saves are
preserved. Public launch remains 1.0.

## Where to find it

Open your player's name button, then Player Development. The Objectives, Skills
and Coach Trust tabs contain progress and the complete rules. Training Focus on
the training screen opens the skill choices directly. Main-menu button alignment,
automatic newspaper/coach flow and the three-shot gate remain in place.

## 1. Career and season objectives

A club-goal target scales with league length, division and tracked previous-season
performance (5–18). The other season objectives are best coach trust of 70 and
finishing among the top three league scorers. The scorer objective is confirmed
at season end from the positive-goal final table, including joint ranks; merely
viewing an early table does not complete it. Completed goals remain recognised,
and the last twenty tracked seasons retain results. Recent summaries are visible.

Career milestones track 50/100 club goals, a completed transfer and a national-team
appearance. Known goals/matches in the current season migrate from older saves,
with neutral trust and untrained skills. Unknown earlier seasons are not invented.
Goals are recognised on load when known current-season counters already meet the
target. Skills and tracked career counters survive season changes and transfers.
Objectives are recognition/progress, not hidden goals or automatic match rewards.

## 2. Focused training and player growth

Choose low finishing, placed finishing, heading or penalties before starting the
mandatory three-shot session. The chosen focus stays locked until the next match
consumes the session; partial sessions resume with the same focus and saved shots.
Heading practice starts at header height; penalty practice uses the penalty spot.
All training remains striker and goalkeeper only, without build-up or defenders.

Completing the three persisted shots gives 12 XP to the selected skill, plus 4 XP
per scored shot meeting the focus: below/equal 0.9m for low finishes, the actual
outer thirds for placed shots, headers for heading, penalties for spot practice.
Other training goals still count towards the normal training result and readiness.
The next level costs 60 + 20 × current level XP. Each skill caps at level 10.

Match benefits are bounded: low normal kicks are 0.6% faster per level when aimed
at or below 0.9m; placed finishing slows normal kick aiming by 1.2% per level;
heading adds 0.1s and slows header aiming by 0.8% per level; penalties add 0.08s
and slow penalty aiming by 0.8% per level. Free-kick controls are unchanged.
The existing launch solver still determines the exact trajectory and collisions.
No target offset, scripted goal, expanded keeper reach or scoring quota is added.

Experience, focus and rewards are saved atomically with training. Failed saves
restore the previous state, and repeated completion/reload cannot duplicate XP.
A failed transfer restores the original club/offer state and milestone count.

## 3. Coach trust, status and playing time

Club trust starts at 50/100. A substitute is below 45, a starter is 45–79 and a key
player is 80+. Training adds 2; each goal adds 6 up to 12; scoring in a key match
adds another 2. A goalless appearance loses 3, or 4 after three missed chances;
without any chances it loses only 1. Trust is clamped to 0–100. A drought can
therefore lower status despite mandatory training; a scoring response restores it.
National games do not change club trust. A new club starts its coach trust at 50.

Substitutes enter at 60 minutes. Starters below 60 trust normally play 75 minutes;
key occasions permit the full match. Trust of 60+ brings 90 minutes. International
appearances retain 90 minutes independently of club trust. Actual interactive
chance minutes are sampled inside that window, accounting for stoppage time;
a late featured chance cannot be moved past the player's exit. Before a chance,
the expected playing time is shown. Coach screens and the hub show current trust.

Role adds a small -0.25/0/+0.25 adjustment to the chance-count centre for substitute,
starter/key player. Existing opponent caps, at most three opportunities, clear and
penalty slots, training's minimum one chance, and morale's two/three chance floors
remain authoritative. No new ordinary-week coach meetings are introduced. Trust
can be recovered; a low-status trained player still gets playable opportunities.

## Validation and limits

371 distinct core and 178 native Kivy cases were validated. The full final core
run passed 370; the final 24-case targeted run includes the added legacy-recognition
case and all progression/localisation tests. The native run passed 177/178; its
old division comparison wrongly assumed no random penalty could be selected. It
now fixes the normal opportunity type for that comparison, and all ten relevant
native tests pass. Earlier compact-training/large-CJK coach findings were fixed
and the affected screen suites rerun successfully.

Coverage includes legacy/damaged extensions, XP caps, three-shot-only rewards,
focus locking and resume, failed-save/transfer rollback, no duplicate rewards,
visible focus criteria, career/season retention, real club match hooks, international
isolation, reachable tabs, draft-name preservation, role minute bounds, recovery
from a drought and retained morale floors. All nine catalogues preserve their
placeholders and bundled font coverage.

The native responsive audit covers 28 views × 11 resolution/density/font settings
× Portuguese/German/Japanese = 924 cases, zero findings. The 132 final training,
coach, profile and development cases replace their earlier rows after the layout
fixes. Goals/skills/trust and compact training screens were visually inspected.
Scrolling is intentional for detailed development information and the trophy list;
newspaper and coach feedback continue to fit one screen.

The actual APK executes focused-training persistence and role checks and passes
exact compiled module/data checks, edition/competition/save/publishing smokes,
existing DEBUG signing, API36/arm64 and 16KB ELF/ZIP alignment. Physical Android
installation and playtesting are pending. This is QA, not a Play production upload
or approval. No server or collection-policy changes were made.
