# Scorer World 0.9.29 — individual crowd jumps and goal celebrations

Every visible supporter now has a stable individual frequency, height, phase and
reaction delay. A per-person fade also avoids a simultaneous landing at the end.
Body and head move together; only the scoring team's fans jump. Height follows
stadium perspective, not screen-density scaling. Stewards remain still. Motion
profiles are computed once per fixture and use no gameplay randomness. Palette
meshes stay batched (at most14 rather than56), without one draw call per person.
Vertices return exactly to their original positions after the celebration.

After a player goal, the scorer runs from his actual shot position to his own
supporters: the home section or the current corner/extended visitor section.
Three visual teammates follow on staggered paths and close around him in an
embrace. They use the player's existing club/national kit and1.80m reference.
The existing match actors, collision positions and ball physics are unchanged.

A decisive-at-the-time goal uses a run, progressively slowing knee slide facing
the supporters, get-up and teammate embrace. The observed rule is a goal taking
the lead from level after80 minutes, or after70 in a final/single-leg playoff.
Two-legged ties with restricted late context are treated conservatively; future
AI goals/results are never inspected or changed. This is not a prediction of the
final winner. Other player goals use the normal supporter celebration.

The match clock stays paused while the sequence plays; automatic result advance
waits for its completion. The existing tap-to-continue still skips it. Goals are
counted immediately and once; no extra attempts, chances, career rewards or AI
scores are added. Training goals and AI goals do not start the player cutscene.
AI goals still animate only the appropriate crowd. Reload/new shot clears the
presentation state; Android texture recovery and all0.9.28 stadium features remain.

Added40 original PNG frames in the established art style: CELEBRATE6, KNEE_SLIDE8,
HUG6, each in front/back views, plus6 sheets. The original168 approved frames are
byte-identical. Total208 PNG frames/30 sheets. Knees slide with folded shins and
fixed-length bones; get-up reuses existing recovery art. The independent Kivy
viewer exposes all11 outfield and8 keeper actions; contact sheets/preview updated.
No Pillow dependency was added to the Android runtime.

Validation:390 core cases completed (387 passed,3 skipped), all201 real Kivy
cases passed, and all4 dedicated asset/clock/articulation/calibration cases pass.
New tests cover independent jump traces, no gameplay RNG consumption, head/body
coherence, still opponents/stewards, exact vertex reset, own supporter targeting,
slide deceleration, get-up/hug phases, no initial position jump, deduplicated goals,
paused clock, automatic continuation, tap skip and no training cutscene. Syntax
checks and exact staging payload checks passed. The standalone viewer checked
all208 frames, three window sizes and zero new textures in2000 warmed updates.

Normal runs/hugs and decisive run/slide/hug scenes at1280x591 were visually
inspected. The real World DEBUG QA APK uses versionCode1026929, API36/min26,
arm64 and the existing upgrade certificate. Exact compiled main/stadium/layout/
celebration/rendering/runtime source, all208 frames/30 sheets and manifest match.
ZIP16KB and all118 ELF alignment checks pass, as do existing edition/ad-free/
safety/competition/save checks. Physical Android installation/playtest remains
pending. No Play submission, production1.0, shot-solver, scoring-rule, save-schema
or server change.
