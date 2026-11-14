# Scorer World 1.0 (1030031)

The rounded net now returns to its original shape with the scored ball still
inside, before collection. Removes the1030030 depth lock that held a permanent
pocket. A resting sphere can remain inside the recovering cloth instead of
pinning it stretched; normal damped spring recovery continues after ball stop.

The solver no longer sleeps at the first quiet frame of a large deformation.
After natural recovery below1cm residual and0.35s quiet, normal settling can
finish at the original rest mesh only if that mesh still contains the ball.
No ball reset, collection shortcut or large shape snap is used. Original rest
coordinates, ground/cord anchors, dissipative contact and finite containment
are preserved. The old rear-contact flag is only a friction state, no shape lock.

21core checks and17native journeys pass. Seven low/high/left/right cases require
EXACT original cloth positions while the ball is still inside and uncollected,
passive ball energy and no premature sleep. A native training update/render
journey verifies the same outcome without modifying authoritative game state.
18additional height/speed/side cases pass energy/bounds/containment. Actual
mobile-detail impact and restored-net screenshots reviewed. Handset acceptance
remains pending. Defender spacing, Coimbra net and whole-ball speed+5% stay.
No backend deployment/save/signing change. Update without uninstalling.
Keep minimum1030030 until Play offers1030031 to every intended player.
Commands: docs/play/FIXES_1030031.md.

Verified delivery:Actions43622630223 reassembled/hash-verified118291172-byte AAB;
Actions43622539790 published uploader1.30. Public uploader/bootstrap/signer and
both native preview hashes match. Private bastion upload and handset acceptance
remain owner-side.
