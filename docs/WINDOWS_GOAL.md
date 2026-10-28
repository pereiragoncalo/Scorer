# Scorer Free Windows0.6.39-win.3 — goal geometry/depth/sponsor slots

Owner reported an undersized goal in Windows, net balls painting over the keeper,
and requested better goal graphics plus a "your company here" sponsorship slot.

Windows goal is12% wider (8.1984m) and10% taller (2.684m), an explicit arcade
playability adjustment, not a claim to official football goal dimensions. One
immutable per-game GoalGeometry profile drives projected frame, net/veil,
post/crossbar collisions, goal-line scoring, aiming clamps and keeper bounds.
The veil arc/path is recomputed for the new height. Android keeps its exact
7.32x2.44 dimensions/path and original goal material. Shared career/ball/post
physical constants, defender/keeper scale, pressure, shot dispersion, chances,
league/NPC goal budget, scores and save schema are unchanged. Windows far-ball
visual minimum is3.5px instead of6px, closer to its physical projected size;
physical ball radius remains0.115m.

The depth bug was the ball.active test: a net ball painted behind the keeper
while moving but jumped to the last/front layer when it stopped. Painter order
now uses position irrespective of activity: behind goal -> before goal frame;
between frame and keeper -> after frame/before keeper; in front -> after keeper.
A glove-held ball retains front-hand rendering. This shared rendering correction
also applies to future Android builds; no Android APK was built in this stage.

Windows frame uses rounded projected white tubes, cool edge shade, subtle highlight,
joint caps, rear support arms and turf-contact shadows. Tube weight follows
projected post radius; net wires are thinner/translucent with distinct side tone.
No opaque net veil, downloaded art, extra colliders or foreground ad boards.

Windows local campaign has exactly4rotating messages: YOUR COMPANY HERE, SPONSOR
THIS STADIUM, SCORER WORLD, WORLD LEAGUES. English-only Free retained; sponsorship
is placeholder copy, not an actual paid advertiser or network. Existing25second
rotation,4texture bound, off-pitch geometry/no click targets remain. Android keeps
its original4message campaign; World has no panels. No network/tracker activation.

## Tests and calibration

161 core/security+92 actual Kivy=253 PASS. New cases cover original exact constants,
new geometry/net paths, real post/crossbar impacts, extended legal mouth and
outside/high misses through real goal-frame collision code, active/stopped ball
layering behind net/between keeper/front, glove possession, render/resize and
bounded local sponsorship rotation. Initial projection test wrongly assumed
world+x maps to screen+x; corrected it to measure projected span. UI/core baseline
and save/edition boundaries remain passing. Static syntax/new-module checks pass.

Paired physical sample:80hard-chance seeds per profile, identical condition and
normalized goal targets, real launch/defender/post/keeper/gravity simulation:
original18/80goals (22.5%), Windows26/80 (32.5%),34keeper saves and20misses. A first
5second harness timeout left1Windows flight unresolved;15seconds resolved it as
a goal, without forcing any outcome. Both final samples have0unresolved. This is
an instantaneous aim bot experiment, not a human success rate or calibration of
whole-season realism; compare docs/WINDOWS_GOAL_CALIBRATION.json. Difficulty was
not lowered by random goal awards/forced misses or score caps.

Staged source smoke passes new-career/training/engine match/save/reload, existing
matchday hub, and a separate static goal render with inactive ball behind the
keeper, enlarged dimensions and placeholder boards. Static scene sets no second
recorded goal; report distinguishes this from gameplay. Native Windows build,
archive/dimension checks and visual capture must pass before final delivery.
Human full-match/audio/shot feel still requires the owner's Windows test.

Files: shot_geometry.py, main.py scoped profile/physics/render changes,
world_promotion.py; Windows calibration tool, frozen smoke/verification/workflow;
core/UI cases; release docs. Original immutable baseline, careers and Android
package/version preserved. Unrelated World/career WIP retained outside release.
Next: replace only the Windows EXE after Save and Exit; Load existing career,
try corners/high shots and check resting net balls stay behind the keeper.

## Verified Windows artifact

Run40740304128/sourcef9b6f05 PASS:6native staging checks, frozen hub/new career/
training/engine match/save-reload/window close-cancel,12visible fixtures, goal
profile8.1984x2.684, inactive ball behind keeper and nonblank hub/goal FBO renders.
[Actual Windows static goal capture](captures/windows-goal.png) visually inspected;
it is an automated render fixture, not a human-played match. The ball aligned
behind the keeper is intentionally occluded by his opaque torso.

EXE41,565,437bytes, AMD64 PE32+, SHA256
`0dd70a7f7f2e5c1def7aad62351e492ea34007cf6aeebc2fd028728937107eac`.
Embedded shot_geometry/profile and depth function verified; active is absent
from the actual frozen depth decision. Fixed Free/empty stats URL/no backend/
keys/saves/World art archive checks PASS. WINDOWS_GOAL_artifact.json retains
exact evidence.253source tests plus6native Windows checks; no physical-user
full-match/audio or signed/store-ready claim. No real sponsor service activated.

[Download Windows0.6.39-win.3](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/windows-beta-0.6.39-3/Scorer-Free.exe).
Use Save and Exit first, replace only the EXE and Load Game; preserve private
%LOCALAPPDATA%/Clemir/Scorer/Free. No career reset or installer required.
