# Scorer World 1.0 (1030039)

Follow-up to continued slow/jerky net animation reported on1030038. Reduce CPU
work in the actual120Hz postgoal contact solver: retain the full swept refit,
then update only faces incident to nodes changed by contact/tether correction.
Unchanged faces retain conservative bounds; exact finite mesh CCD/contact and
containment remain. Unroll equivalent3D arithmetic and freeze camera values once
per dynamic net draw batch rather than reading widget properties per vertex.

No ball-speed multiplier, damping/material/timestep change or simpler collision
geometry. Keep38audio/static-stage optimizations,37jumping headers, saves,
scoring, net anchors/seams and recovery. No backend patch or new art/signing key.

Host CPU profiling: mean postgoal frame35.05ms on38vs22.34ms on changed source
(includes cProfile overhead). This is not Android FPS and does not establish
handset resolution. See docs/OPPORTUNITY_PERFORMANCE.md for evidence/limits.
Phone acceptance remains owner-side.39stays optional until genuinely available
in Play; minimum38is retained. Bastion instructions: docs/play/FIXES_1030039.md.

Final source validation:58core/physics/staging/publisher tests pass(one hostJDK
skip);27native UI tests pass; final pinned-publisher suite25pass(one hostJDK skip).
1080sampled ball position/velocity/net-displacement values are bit-identical
to38after preserving original floating-point sum semantics.

Corrected Android39build/audit pass:unsigned World/production metadata,16KiB
native/ZIP/inspection alignment, exact compiled runtime and248frames/35sheets.

Public delivery verified: AAB run43754644723 and automation v1.38 run43754586318
succeeded. Public bootstrap/uploader/signing-helper SHA256 hashes match pins;
AAB asset123953016bytes matches audited manifest. Transfer commit was resumed
after publishing its source parent; existing immutable blobs/checksums reused.
Private signing/Play submission and handset performance acceptance remain pending.
