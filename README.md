# Scorer0.6.44 QA candidates

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

Verified179core/security+99Kivy PASS (278unique tests). Native run41241589273/
sourceb4137e3 passed6staging checks and frozen functional/render smoke, with real
Windows minimize/restore callback path giving foreground_openings_test=2. Probe
is isolated, uses failed fake transport, never posts to owner. Both actual Android
packages inspected with matching Python3.14: on_start/on_resume begin_session and
on_pause pause_session present. Original debug upgrade signature, target36/min26,
ZIP16KB/118ELF16KB and no advertising SDK in DEX verified. No actual phone-human
opening test claimed; owner should verify on own device. No server/credentials/
DNS or manual-counter changes made; same existing endpoint/protocol.

[Scorer-Free-0.6.44.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.44/Scorer-Free-0.6.44.apk)

[Scorer-World-0.6.44.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.44/Scorer-World-0.6.44.apk)

[Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.44/Scorer-Free.exe)

Upgrade in place after Save and Exit, Load Game. Stats require prior Privacy consent. Owner panel refreshes only on Load totals; count sessions is a daily aggregate. No server upgrade required, no adverts, preserve careers. Debug Android/unsigned Windows; not a production Play release.
