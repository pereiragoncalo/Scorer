# Scorer World 0.9.26 — approved retro footballers

The approved art revision 2 now replaces the procedural field players and
goalkeeper in the existing game. Original pixel sprites retain clear dark
outlines, fixed proportions, articulated limbs, limited palettes and nearest
filtering. The exact approved 168 PNG frames and 24 sheets are shipped unchanged.
Team shirt, trim, shorts and socks use the existing match-kit colours; the keeper
retains the existing contrasting kit selection, long sleeves and gloves.

Run and dribble follow the existing build-up movements. Pass/kick contact frames
match the existing release events; the hero winds up while aiming and advances
to contact on the immediate shot event. Headers follow the existing header shot.
The existing rebound blocker uses the tackle animation. This adds no new tackle
control or fall mechanic: the fall clip remains available for an actual future
fall event, rather than making actors fall for decorative reasons.

Keeper steps, low/high saves, both dive directions and catches follow existing
keeper state. Dive hip anchoring removes duplicate authored root travel. During
a held-ball forward fall the whole sprite rotates without stretching its limbs,
and the gloves follow the original held-ball position. Recovery plays only after
a completed result with an inactive, unheld ball, so the visual stand-up cannot
change a live save. The ball stays a separate physics/rendered object.

Only the three existing character drawing methods changed, plus a lazy renderer
accessor. All 135 other existing game methods, including movement, launch,
fixed-step physics, controls, field-player hitboxes, goalkeeper skeleton/capsules,
held-ball attachment, scoring, training gates and opportunity timing, were
unchanged. No save migration, gameplay balancing, goal-budget or server change.

The animation/texture implementation is shared by the standalone viewer and game
through root runtime modules. Android excludes developer tools, so no runtime
imports from tools or Pillow are required. A bounded 24-texture recolour cache
reuses atlas textures across frames. The Android staging allowlist now explicitly
includes assets/sprites/manifest.json, with a regression test checking exact art.

Validation: 385 core cases completed (382 passed, 3 skipped); all 192 native Kivy
cases and all 3 dedicated asset/clock/articulation cases passed. Integration tests
verify drawing never changes ball/player/keeper state, all save states render,
shot contact remains immediate, team palette ordering, two-actor training and no
texture uploads in warmed repeated draws. Existing opportunity/training/catch
regressions also pass. 1280x591 screenshots of aiming, build-up, shots, dives,
catches and training were inspected. See docs/sprite_lab/integration/ for the
captures and desktop timing/memory measurement. A same-process software-rendering comparison measured 35.1 ms/frame with sprites
and 34.9 ms with the prior procedural renderer; CPU canvas drawing was 11.45 ms
and 11.85 ms respectively. No warmed texture uploads occurred. An earlier run
under concurrent test/build load took 104.9 ms/frame, illustrating host variance.
These are desktop tests, not physical Android performance measurements.

The actual World DEBUG QA APK was built with versionCode 1026926, API36/min26,
arm64-v8a and the existing upgrade certificate. Signature, ZIP16KB and all118
ELF alignment checks passed. Actual APK inspection verifies exact approved art,
compiled main/renderer/clock/texture code, edition, ad-free/billing-free metadata,
existing saves/competitions/training/newspaper rules. Developer sprite tools are
excluded from the APK. Physical Android installation and playtesting remain
pending. This is a QA upgrade; no Google Play submission or production1.0 change.
