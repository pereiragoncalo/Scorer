# Free0.6.39 — anonymous session start/end notices

Owner preference: email at session start/end instead of a daily summary.
Added sessions_ended to the whitelist (nine counters total); normal on_stop marks
it once after an opted-in start. Pause/resume do not create fake endings/starts.
World no-op adapter includes end_session and remains transport/config-free.
An explicit flush while another upload is running now requests one follow-up so
normal stop cannot silently drop its newly saved end event behind an in-flight
start. Offline counts remain private for later upload; opt-out stops and erases.
No background service, device ID, player identity or per-session timestamp added.

The server-only session_notices command reads aggregate totals, previews by
default and only emails new starts/ends with explicit --send. Successful sends
checkpoint day/event/count; failure leaves pending totals. --baseline skips old
history without emailing. Other counters alone do not trigger notices. One
operator can schedule every minute after configuring real HTTPS hosting and
SMTP. Multiple arrivals may share a notice; no start/end pairing or duration is
possible. Original daily digest is available but should not also be scheduled.
Recipient remains in private deployment config, not public source or APK.

Android may kill a process without on_stop, or interrupt a daemon upload. A
normal-end notice is therefore best effort, potentially delayed until next run.
Never infer a crash ended normally. Network/SMTP acknowledgements can be lost,
causing duplicates; email polling/global ingestion must be bounded against spam.

Validation:148 core/security +80 actual Kivy tests PASS (228), covering start/end
once, no background-end, in-flight follow-up, preview/no-send, delta checkpoint,
SMTP failure/baseline, mocked SMTP with verified STARTTLS and server-only auth,
existing privacy/career/offline/World boundaries. No real email or public host
used in tests. Actual arm64 Free APK0.6.39/code1026639 built; package/certificate/
API36/empty endpoint/backend exclusions/ZIP16KB/118 ELF checks passed. No physical
phone test. Earlier daily digest text assertion was updated for explicit start
wording; the first attempt to run UI with xvfb-run failed because it is absent,
then tests ran through the available SDL2/Mesa Kivy provider.

Files: anonymous_stats.py, main.py, menu_ui.py, tools/prepare_editions.py,
buildozer.spec; server/usage_digest.py, session_notices.py, Dockerfile.usage,
USAGE_SETUP.md; core/UI tests; policy drafts, README/AGENTS/build log/artifact.
Unrelated World/career WIP remains outside the tested snapshot. World actual
latest APK stays0.6.37. No public Play release, real ads or payment activation.

Next: phone validation, configure hosting/TLS/SMTP privately, deploy/test with
fake reports, then build a configured opt-in Free beta. Current receiving URL is
empty: local optional counters only, no emails or uploads have been activated.
