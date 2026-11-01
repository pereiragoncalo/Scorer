# Data Safety — Scorer World 0.6.47

Owner-approved public identity: **Gonçalo Pereira**, **goncalo@clemir.com**.
Scorer World is **free**, ad-free, with the names editor and no in-app purchase. Account verification
is confirmed by owner. Console forms have not been submitted in this session.
Windows is not a Play listing. Only com.clemir.scorerworld is the current Play product.

| Flow | Actual implementation | Form considerations |
| --- | --- | --- |
| Careers/exports/editor/language | Private local files; explicit user-selected SAF documents; no cloud career upload | Local-only data is not an automatic server collection. User-chosen document provider can be cloud-backed; disclose user-directed export. Export contains names/progress, excludes credentials |
| Automatic usage |9 numeric app activity/failure counters. No ordinary switch; applicable privacy requests suspend collection. Send begins after detailed first-run notice acknowledgement, not a consent claim | Required App interactions / analytics; assess Diagnostics for selected failure counts. Never declare optional or no data collected |
| Collector and provider |90day combined receipt-day totals,7day local expiry; hourly active cleanup/daily maintenance. Collector has no raw requests/IP/UA logs; Cloudflare processes network/IP | Owner confirms only Tunnel/proxy, no Web Analytics/Logpush; provider may process IP/security data under its own terms. No direct account audit was performed. Review applicable retention and transfer terms. Do not automatically infer location collection from an IP, or omit actual inference. Not all retained data is ephemeral |
| Privacy rights cases | Created only on explicit request; private random token, server hash/reference/status/dates; not linked to usage. Pending retained until resolved, resolved pruned after 90 days; no aggregate backup | Assess Other user-generated content and identifier type for request credential; support/compliance purpose. Usage remains a required flow for ordinary use, not an optional analytics switch |
| Optional completed records |Explicit adult-managed public access + terms v1 + Share; chosen name/team, season, matches, goals, country/division/edition; persistent ownership token only for writes/deletion | Names include nicknames in Google definition. Assess Name, other UGC/activity and identifier type for random persistent token; it is not anonymous merely because random. Device/session IDs are absent from usage payload, not a claim that ranking has no identifier |
| Public IDs and local blocking |Opaque public publisher/record IDs; blocked publishers stored locally, filtered from display | Declare identifier handling accurately; public IDs cannot authorize writes/deletion |
| Reports/moderation |Reporter token hashed on server; target publisher ID and fixed reason only. Reports30days, names pending until approved, suspended publisher ID retained until lifted | Other user-generated content/identifier handling, safety/moderation purpose. No free-text report or raw diagnostics. Human operator still required |
| Family controls |Birth date checked locally then discarded; PIN salted hash/local settings; fail lockout | Not uploaded. Self-declared adult action is not verified parental authorization/identity. Confirm children/social treatment before release |
| Removal/backups |Own records/reports removed on withdrawal; offline pending retry on next refresh. Managed backup copies only totals; expires7days. Local export user-controlled | Explain deletion/support. No email/password account; still assess whether persistent public identity falls within Play account-deletion definition. /delete public support instructions prepared |
| Advertising/billing |Absent SDKs, ads and purchases |Contains ads=No; no in-app purchases. World free per owner |

HTTPS is verified. Collected/shared/ephemeral classifications must follow current
Play definitions, including service-provider and user-directed sharing exceptions;
do not automatically label all transfers sharing or all aggregates ephemeral.
The same data type cannot be declared optional when some automatic flow requires
it. Usage payload's historical `app:scorer_free` is a common family constant, not
an edition/platform/unique-player breakdown.

Public policy URL: https://stats.clemir.com/privacy. The previously installed draft is not this final policy; install the new server and English policy using WORLD_LAUNCH_0.6.47.md. Confirm the live published marker after deployment. Console form classifications must match the actual shipped build and deployment. No SMTP service is activated.
