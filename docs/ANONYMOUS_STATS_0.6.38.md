# Free0.6.38 — optional aggregate usage statistics

Implemented an independent, default-off opt-in in Privacy for eight fixed counters.
No names, club identities, saved careers, contacts, player email, locale, precise
session timestamps, advertising IDs or persistent installation/report IDs enter
the payload. Private local counters are atomic, bounded and expire after7days
on next use. Withdrawal stops new counts and erases pending data, including a
fail-closed path if preference writes fail. Careers are never changed by this
choice. World staging replaces the collection module with a no-op adapter and
removes its destination configuration.

Free lifecycle records sessions, accepted new careers, successful explicit loads,
completed weekly training/matches, player goals and fixed load/save failure counts.
No repeated reward/match completion inflation; no simulation RNG or match changes.
The HTTPS-only sender is nonblocking, rejects redirects, verifies TLS and preserves
unsent data offline. No automatic background schedule. Counters are approximate;
acknowledgement loss can duplicate contributions. No unique-user claims.

The stdlib own collector validates exact small payloads, aggregates immediately
into SQLite(day,event,count), has bounded traffic/timeouts, suppresses request
logging and removes90day aggregates on accepted uploads. Owner totals require a
server token. Server-only optional daily email digest uses STARTTLS and no app
credentials. See ../server/USAGE_SETUP.md for deployment, SMTP and privacy limits.

## Actual release state

Built arm64 Free APK0.6.38/code1026638. Its ENDPOINT is EMPTY: enabling the option
retains counters locally and sends nothing. No collector was deployed, no owner
summary email was sent, no production AdMob or payments were enabled. Actual
hosting/TLS, SMTP settings, a public policy and Play disclosures remain pending.
Recipient choice is saved privately outside Git. World latest APK remains0.6.37.

143 core/security tests +79 real Kivy UI tests passed (222). New tests cover
opt-in/off/expiry/scope/atomic failures, isolated World, payload/URL restrictions,
failed and successful sends, late events/withdrawal, real localhost HTTP ingestion,
rejected PII, protected totals, email preview/header validation and real UI event
hooks. HTTPS across a live public host, SMTP delivery and phone usage were NOT
tested. APK signature, package/version/API36, actual bundled default endpoint,
World/backend/private-data exclusions, ZIP16KB and native ELF alignments checked.
The first verifier incorrectly treated compressed libpybundle.so as ELF; corrected
the verifier to inspect the actual ELF members; no APK change was needed.

Modified main.py/menu_ui.py hook/privacy UI; anonymous_stats.py/analytics_config.py;
tools/prepare_editions.py, buildozer.spec and .gitignore; server collector/digest/
deployment examples; tests/test_anonymous_stats.py, tests/test_usage_collector.py,
ui_tests/test_usage_statistics.py; privacy/data-safety drafts and release docs.
Unrelated pending World competition/career work is preserved outside this tested
release snapshot. No real-device result or Play-ready production claim is made.

Next: install the linked Free APK over the earlier Free, check Privacy opt-in and
erasure without changing your career; configure real hosting and SMTP privately,
then build/test a destination-specific beta before enabling production uploads.
