# Scorer World 1.0 (1030027)

Corrects the interpretation of the requested 5% speed increase. Normal real-time
match, player, goalkeeper, aim/countdown, celebration and net clocks are restored.
Only player shots during opportunities use flight duration/1.05, with the existing
gravity/drag solver retaining the selected target. This applies to training,
match shots and headers; goalkeeper tip redirects retain their original solver.
Fixed-step physics quantises the requested flight duration to its ordinary tick.

Coimbra Preto is explicitly assigned the rounded loose hexagonal 3.50 m net by
its stable UID6d0a94b6d9d584ce77e0. The assignment survives custom club names and
existing careers and applies to home matches and training. Away fixtures use the
actual home stadium. All nine net styles remain available.

Ten pure flight/clock/geometry/assignment tests and14 native opportunity/clock/
geometry journeys pass, including penalties, long shots and cross headers in
both training and matches. Physical Android acceptance remains pending.
Same package, save format and owner signing identity. No backend deployment.
Update via Play without uninstalling. Keep minimum1030022 until Play actually
offers1030027 to all intended players. Commands: docs/play/FIXES_1030027.md.

Verified delivery:Actions43592176698 reassembled/hash-verified118286990-byte AAB;
Actions43592113808 published uploader1.26. Public uploader/bootstrap/signer hashes
match. Private bastion upload and physical Play acceptance remain owner-side.
