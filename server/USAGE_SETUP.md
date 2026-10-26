# Optional Free usage collector and email summaries

Status: prepared and locally tested, NOT deployed. The Free0.6.38 APK has an
empty endpoint; optional counters remain local even after opt-in. World has no
collection client. No email has been sent. A mailbox receives summaries from
this server; it cannot replace the HTTP collector.

## Server deployment

Use a maintained server, Python3.10+, private writable storage and a real HTTPS
hostname. From the repository root:

    python server/usage_collector.py --db /absolute/private/usage.sqlite

Default bind127.0.0.1:8080; put a TLS reverse proxy in front. The Caddy example
is a placeholder, not an installed service. Disable request/error/access logging
at the reverse proxy, hosting provider and collector; assess unavoidable hosting
processing of IP addresses. Publicly expose only POST /v1/usage, not the owner
report route. Add bounded proxy request size/timeouts and monitor aggregate
storage without logging request bodies or client addresses. The collector has
5s connection timeouts,16 concurrent connections, a20requests/s global bound
and a4096byte body limit. Public counts can be forged: not billing/fraud metrics.
Dockerfile.usage is provided as an alternative, but its image was not built in
this stage. Do not expose this temporary development workspace as the service.

GET /health is for local health checks. GET /v1/totals is disabled unless
SCORER_STATS_ADMIN_TOKEN is set on the SERVER; when enabled it requires that
Bearer token. Generate/store it privately, never add it to the APK or Git.
The SQLite totals table contains only(day,event,count), grouped by UTC receipt
date; no raw reports, addresses, user agents, identifiers or player data.
Aggregates older than90days are removed on a subsequent accepted POST.

## Build with a real receiving URL

After deploying and testing HTTPS and updating/publishing the privacy policy:

    python tools/prepare_editions.py --edition free --output /absolute/clean-staging --analytics-endpoint https://YOUR-HOST/v1/usage

Check --help for the staging argument syntax if the tool changes. HTTPS on443,
exact path /v1/usage, no credentials/query/fragment. The default is deliberately
empty. The player must explicitly allow optional statistics in Privacy. Changing
the URL resets consent and erases old local counts; do not silently migrate local
consent to a remote destination. Verify certificate trust and actual consent/
withdrawal on an Android phone before rollout. Advertising consent is separate.

## Email (server-side only)

Keep all SMTP settings in a protected service environment outside the repository:

    SCORER_STATS_MAIL_TO=OWNER-MAILBOX
    SCORER_STATS_MAIL_FROM=VERIFIED-SENDER
    SCORER_STATS_SMTP_HOST=SMTP-HOST
    SCORER_STATS_SMTP_PORT=587
    SCORER_STATS_SMTP_USER=SMTP-USER
    SCORER_STATS_SMTP_PASSWORD=SERVER-SECRET

The owner's chosen recipient is saved privately in the workspace configuration,
not hardcoded in the APK or published source. Missing sender, host and SMTP
credentials remain to be configured by the server operator. Never send passwords
in chat. The sender must be permitted by the SMTP provider (SPF/DKIM as needed).

Preview yesterday's UTC aggregate summary without sending:

    python server/usage_digest.py --db /absolute/private/usage.sqlite

After explicit operator activation, --send sends via verified STARTTLS. Schedule
one daily invocation after midnight UTC using a single operator/cron instance.
The digest records acknowledged sends by date to avoid ordinary repeat sending;
ambiguous SMTP failures or concurrent operators can still duplicate a message.
No mail is sent by the app, and no player email is requested. Agree mailbox and
provider retention/access rules; the collector's90day purge cannot erase emailed
copies. No live SMTP delivery or scheduled job was tested/activated here.

## Interpretation/privacy limits

Eight optional fixed counters: sessions, new_careers, careers_loaded,
trainings_completed, matches_completed, goals_scored, load_failures, save_failures.
No unique users, installations, retention cohorts or conversion attribution can
be inferred. Offline reports may arrive later, grouped by receipt date; ambiguous
HTTP acknowledgements can duplicate counters. They are approximate totals.
Local unsent counters expire after7days on next use; opt-out clears them. An
already running request may finish after withdrawal. The server cannot erase
one contribution later because it stores only combined totals. Complete the
actual Play data-safety/children/privacy assessment before production activation.
