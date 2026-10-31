# Scorer0.6.44 — every opening counts

Previous code counted once per process, only after touching the splash. Android
background/resume left the same _session_counted flag set, so opening again gave
no second increment. Owner explicitly requires two openings to count as two.

Now an opening is app startup (before splash tap), or return from a background
pause; duplicate on_start/resume/splash notifications in the same foreground
interval do not increment twice. Windows binds minimize/restore to the same
lifecycle. Normal session-end counter still means normal app termination, not
every background pause, so starts/ends are not paired duration or active-user data.

With existing optional consent enabled, increment is atomically persisted before
sending; startup/resume immediately flush. Pending counts retry every10seconds
while Kivy is active, in addition to existing pause/exit flush. Failed traffic
remains pending across process restart (existing7day expiry/withdrawal scope).
No new identifiers, raw opening timestamps, player/device/session log or endpoint.
Same installed collector /v1/usage stores daily SUM counts; two openings are
sessions=2 in that day's row, not two people or two raw history rows. Existing
admin page loads a snapshot: press Load totals again for new server values.

No server upgrade is needed. No synthetic correction was applied to owner totals:
unrecorded historical openings cannot be recovered reliably. Offline display can
lag until delivery; a force-stop/network timeout can interrupt acknowledgement,
so existing protocol still cannot promise mathematical exactly-once delivery
under ambiguous acknowledgements. No fake claim that local increment guarantees
an instantaneous remote update without connectivity.

Tests reproduce launch before splash, warm pause/resume, duplicate notifications,
queued first cold start then second start, normal end idempotency and withdrawal.
Real local HTTP collector test verifies TWO received openings aggregate to2.
Native frozen Windows smoke runs minimize/restore callbacks with isolated opt-in
probe sender that never reaches owner server, then restores default-off real
usage before game stops. Other saves/gameplay/ads-free/ranking remain unchanged.
Next: upgrade, keep existing consent, open twice, then reload private totals;
confirm count increases by2 relative to its previous value.
