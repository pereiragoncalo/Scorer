# Scorer World1.0 (1030037)

Heading attempts now show preparation, take-off, airborne forehead contact and
landing. A0.22s input wind-up freezes the chosen aim/countdown, ignores duplicate
inputs and launches once at the authored contact frame. The existing approved
8-frame header art now moves relative to one fixed contact calibration rather
than pinning every pose's forehead to the ball. Feet leave the ground and the
shadow stays on the pitch. Shared cross reception/header launch height is2m to
match the airborne contact; the ordinary launch solver still resolves the aimed
trajectory and existing ball-speed+5%. This changes the physically appropriate
header launch height, so handset finishing acceptance remains pending.

Kicks/penalties launch immediately as before. Context help pauses the wind-up;
new chances/reset discard stale queued shots, pressure keeps advancing normally.
Calendars, net physics, stats/leaderboard, saves and original signing retained.
No new art/assets or backend patch. Exact existing art remains approved.
Keep minimum1030032 until actual Play availability. Commands: FIXES_1030037.md.

Validation:47pure/staging/calendar/publisher tests pass(one hostJDK skip),13native
header/contact/renderer/keeper/training tests pass. Android AAB audit passes
118ELF16KiB, exact compiled runtime source and approved resources/ZIP alignment.
