# Opportunity slowdown investigation — 2026-11-15

Baseline 7dbd3d2 (Android1030037 source). No Android release/version policy change
in this investigation. No phone trace/ADB available; host CPU profiling is not
proof of handset FPS or of the only cause on the owner's device.

Findings and corrections:
- Static seats/concrete geometry was cached as Python arrays but recreated and
  uploaded as new Kivy Mesh objects every frame. Retain/reattach one clearable
  InstructionGroup until stadium/camera/viewport geometry changes. No FBO.
- A goal constructed ClothContacts topology on the gameplay thread. Prepare it
  alongside the visible cloth, reuse it and refresh current bounds at handoff.
- Idle cloth unnecessarily rebuilt contact bounds each120Hz step. Skip only
  when neither cloth motion nor actual contact changed the mesh.
- Deformed net projection evaluates thousands of strand points. Unroll identical
  weighted sums/projection arithmetic to remove generator/dot-call overhead.
- First goal synthesized51817 audio samples, wrote WAV and loaded SDL audio
  synchronously. Production staging37 lacks the generated root WAV. Generate
  the same waveform in a worker at App startup, atomically cache it in writable
  app data, then load on Kivy's thread. A goal only plays prepared audio; if it
  is not ready it skips sound instead of doing IO/synthesis on the goal frame.

Amplifiers kept unchanged:
- simulation_dt clamps a delayed frame to120ms. A sustained frame above that
  threshold loses simulation time and makes all action slower in wall time.
  Keep the background-return safety cap; reduce hot-path work rather than
  raising catch-up work and risking a physics backlog.
- Delivery durations are deliberately1.9–3.15s; short passes can therefore be
  physically slow even at steady FPS. Existing+5% ball-only multiplier remains.
  No extra speed/difficulty/aim/calendar/save/net-contact changes in this patch.

Reproduce: SDL_VIDEODRIVER=offscreen SDL_AUDIODRIVER=dummy KIVY_NO_ARGS=1
/workspace/striker-venv/bin/python tools/profile_opportunities.py
Optional SCORER_PROFILE_BASELINE points to an export of the five changed baseline
runtime modules. The harness uses actual Kivy update/draw but no GPU presentation
or phone; training/no crowd, rounded hex net,1280x720,30buildup/40postgoal frames.

Paired cProfile run on this host (timings INCLUDE profiler overhead):
| CPU measurement |1030037|changed source|
|---|---:|---:|
|Mean buildup update/draw|10.91ms|4.35ms|
|Goal handoff (unprofiled)|7.20ms|0.37ms|
|Mean postgoal update/draw|52.81ms|34.45ms|

Absolute times vary with host load. Do not convert these into Android FPS.
Logs: striker-runtime/performance38-paired-{before,after}.log outside checkout.

Validation:23cloth/contact/travel/rolling tests;27native UI net/header/training/
stadium/performance tests;8audio/opportunity/staging tests pass.1080samples of
ball position, velocity and net displacement are bit-identical to baseline
across box/veil/rounded nets and12/30m/s shots. Syntax/diff checks pass.
Initial native run found a test cleanup race when workers were started by widget
construction; fixed by starting preload in the real App.on_start instead.
Android compilation and owner handset acceptance remain pending.

## Follow-up after1030038 handset feedback

Owner reports both slow motion and stutters remain.38is therefore not accepted
as a handset performance fix. Further source changes target the simulation,
not a playback-speed multiplier or softer/less accurate net:
- Full swept broad-phase refit remains once per moving cloth step. Subsequent
  contact corrections only refit faces incident to touched/contact or tether
  nodes. Other faces retain safe conservative swept bounds. Exact current cloth
  triangles and moving-sheet CCD still decide all contacts/containment.
- Freeze camera values once per dynamic net projection batch, instead of reading
  widget camera properties for every strand vertex.
- Scalar3D vector/spring arithmetic avoids inner generator/axis-loop overhead,
  retaining operation order and the original120Hz integration/coefficients.

Same local profiling harness against exported38source: mean postgoal CPU frame
35.05ms ->22.34ms; maximum65.75ms ->33.99ms in this short sample. Timings INCLUDE
cProfile overhead and are not phone FPS. New full-refit/partial-refit regression
compares ball/velocity/cloth positions through120steps in all three net shapes.
Handset outcome remains unverified until39is installed and tried by the owner.
