# Scorer World 1.0 (1030004)

Adds a server-controlled mandatory update screen with the chosen offline policy:
play is allowed without internet unless an already known minimum requires update.
Includes the transactional backend installer and pinned bastion signing helper.

See UPDATE_GATE_1030004.md for installation and future minimum controls.
The unsigned AAB requires the existing owner's upload certificate. Delivery here
is not a Play submission; bastion owner executes the verified installation block.
Existing 1030003 users must update once before this mechanism is available.
