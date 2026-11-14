# Scorer World 1.0 (1030023)

Side-net contact preserves tangential ball travel.1030022 rewound the complete
sphere to the swept time of impact, losing the remainder of the step even along
the side panel. A reproduced18m/s glancing shot moved at7.98m/s while its stored
velocity remained17.81m/s. Only through-sheet normal travel is now clipped;
tangential travel is retained. Free flight keeps its incoming speed with normal
air drag until a real visible-mesh contact. Reference-net recovery no longer
injects inward normal springboard momentum into a spent ball.

Goal handoff reuses the existing cloth instead of constructing and discarding
another cloth/contact mesh. Cached mesh projection is independent of the moving
ball overlay; finite triangle bounds avoid nested generator work.

18 pure physics/shape tests and19 native Kivy integration tests pass, including
glancing speed, free flight, triangular containment at multiple heights/speeds,
passive energy, stable occupied pockets, unchanged physical ball/scoring and
unchanged4+3 defensive shape/training. Two focused handoff/cache checks also pass
with constructor-call tracking. Android device acceptance remains owner-side.

Same package, career/save format and owner upload certificate. No backend patch.
Publish to internal only. Keep the known available1030022 as mandatory minimum
until Play offers1030023 to every intended player. Update without uninstalling.

Download: https://github.com/pereiragoncalo/Scorer/releases/tag/world-1.0-1030023
Commands: docs/play/FIXES_1030023.md

Verified public delivery: Actions43576375982 reassembled/hash-verified and attached
the118244501-byte AAB. Actions43576309964 delivered uploader1.22. Public uploader,
bootstrap and signer download hashes match. Private bastion signing/upload and
actual Play/Android availability remain owner-side.
