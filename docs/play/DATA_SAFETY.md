# Play data inventory — current separate apps, draft declarations

Free com.clemir.striker and World com.clemir.scorerworld must be assessed separately.
Do not reuse historical single-app purchase/token/installation-ID disclosures.
No current APK ships Google Play Billing or the legacy purchase-verification client.

| Flow | Current treatment | Declaration review |
| --- | --- | --- |
| Player/club names, careers, fixtures, aliases | Private local files; no game upload | No developer collection through this flow |
| World locale | Local phone-language/country suggestions and manual UI language; no GPS | Not uploaded |
| Google ads in Free | Child/under-age, G/non-personalised requests; IP/app-device/diagnostic/ad data can go to Google; AD_ID/AdServices permissions absent | Review actual SDK disclosures; no AD_ID does not mean no collection |
| Optional Free usage counters | Default off; no identifiers/free text/session timestamps; only9 allowlisted numeric counts; unconfigured beta is local-only | If HTTPS destination is activated, review optional app-interaction/diagnostic collection, analytics purpose, encryption, consent, ephemerality and actual infrastructure. Calling it anonymous does not remove declaration duties |
| Collector network | IP is transiently visible in transport; prepared service stores only UTC receipt-day/event/count totals | Verify reverse-proxy/CDN/error logs and host processors too; do not claim global zero-IP processing |
| Owner email digest | Server-only optional daily aggregate summary; no player's email or SMTP credential in app | Identify real email processor/retention before publication; no mail has been sent merely by preparing code |
| World | No ads SDK, counter transport/config or Internet permission | Separate app assessment; local editor/storage remain |
| Backups/editor | Private backups and user-chosen SAF exports; cloud backup disabled | Explain uninstall/delete and document-provider handling |

The counters are session starts and normal ends, new/loaded careers, completed training/matches, player
goals and selected load/save failures. They are not unique users, exact installs,
retention measurements, stack-trace/crash reporting or billing/revenue statistics.
Current beta has no collector URL and sends no developer-usage telemetry. Future
configured builds require explicit per-player opt-in and a recipient-scope reset.
Counter/file/schema validation rejects unknown fields and identifier labels.

Prepared local counters expire after7days on next use; prepared backend keeps only
90days of aggregate daily totals. Approximate receipt-day counts may include late
offline batches/ambiguous-ack duplicates. No raw reports or individual lookup key.
Actual hosting/SMTP service is not deployed by this repository. Keep the public
privacy policy, audience/Families status and Play Console answers aligned with the
real build/SDKs/services; this file is not a submitted or approved declaration.

Session-notice update0.6.39: an additional sessions_ended counter records normal
application stops once per process, only after an opted-in start. Backgrounding
alone does not end a session; force-stop/crash may omit it. Server-only owner
email notices may summarize newly received starts and ends, batched per polling
interval, without IDs or matching individuals. Receipt time is not exact event
time. Notices/SMTP are not deployed or active in the current empty-endpoint beta.
