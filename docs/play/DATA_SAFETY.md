# Data Safety inventory — Scorer World1.0 candidate (0.9.39 content)

Owner-approved public identity: **Gonçalo Pereira**, **goncalo@clemir.com**.
Scorer World is **free**, ad-free, with the names editor and no in-app purchase. Account verification
is confirmed by owner. Console forms have not been submitted in this session.
Windows is not a Play listing. Only com.clemir.scorerworld is the current Play product.

| Flow | Actual implementation | Form considerations |
| --- | --- | --- |
| Careers/exports/editor/language | Private local files; explicit user-selected SAF documents; no cloud career upload | Local-only data is not an automatic server collection. User-chosen document provider can be cloud-backed; disclose user-directed export. Export contains names/progress, excludes credentials |
| Optional usage |9 numeric app activity/failure counters, disabled by default and migrated off for old mandatory builds. Separate adult PIN opt-in in Help > Settings; Stop Statistics & Erase Unsent requires no PIN. Launch acknowledgment does not enable analytics | Optional App interactions / analytics; assess Diagnostics for selected failure counts. Never declare no data collected while opt-in collection is available |
| Collector and provider |90day combined receipt-day totals,7day local expiry; hourly active cleanup/daily maintenance. Collector has no raw requests/IP/UA logs; Cloudflare processes network/IP | Owner confirms only Tunnel/proxy, no Web Analytics/Logpush; provider may process IP/security data under its own terms. No direct account audit was performed. Review applicable retention and transfer terms. Do not automatically infer location collection from an IP, or omit actual inference. Not all retained data is ephemeral |
| Optional completed records |Explicit adult-managed public access + terms v1 + Share; chosen name/team, season, matches, goals, country/division/edition; persistent ownership token only for writes/deletion | Names include nicknames in Google definition. Assess Name, other UGC/activity and identifier type for random persistent token; it is not anonymous merely because random. Device/session IDs are absent from usage payload, not a claim that ranking has no identifier |
| Public IDs and local blocking |Opaque public publisher/record IDs; blocked publishers stored locally, filtered from display | Declare identifier handling accurately; public IDs cannot authorize writes/deletion |
| Reports/moderation |Reporter token hashed on server; target publisher ID and fixed reason only. Reports30days, names pending until approved, suspended publisher ID retained until lifted | Other user-generated content/identifier handling, safety/moderation purpose. No free-text report or raw diagnostics. Human operator still required |
| Family controls |Birth date checked locally then discarded; PIN salted hash/local settings; fail lockout | Not uploaded. Self-declared adult action is not verified parental authorization/identity. Confirm children/social treatment before release |
| Removal/backups |Own records/reports removed on withdrawal; offline pending retry on next refresh. Managed backup copies only totals; expires7days. Local export user-controlled | Explain deletion/support. No email/password account; still assess whether persistent public identity falls within Play account-deletion definition. /delete public support instructions prepared |
| Advertising/billing |Absent SDKs, ads and purchases |Contains ads=No; no in-app purchases. World free per owner |

HTTPS is verified. Collected/shared/ephemeral classifications must follow current
Play definitions, including service-provider and user-directed sharing exceptions;
do not automatically label all transfers sharing or all aggregates ephemeral.
Classify each data type across all actual flows; optional usage does not make data required for an enabled online feature disappear. Usage payload's historical `app:scorer_free` is a common family constant, not
an edition/platform/unique-player breakdown.

Public policy URL for the new candidate: https://pereiragoncalo.github.io/Scorer/privacy/.
Public legal pages are hosted by GitHub Pages; GitHub receives site-request/IP data
when a browser visits them, as disclosed in the policy. Gameplay requests still use
stats.clemir.com/Cloudflare. The old server policy is not automatically updated by
the independent website deployment. Verify final Pages availability before submission.


## Current candidate additions,9November2026

-Optional public records now have separate Season and Career categories, using
 the same adult-managed sharing/moderation and owner-token model. Career totals
 are club-career totals. Viewing does not publish records.
-Lifestyle purchases, fictional wages and generated estate portraits are local.
 These are not real financial transactions or uploads of the user's photographs.
-Feedback opens an external email draft to public support with a subject only.
 The game does not transmit a feedback form, email identity, logs or attachments.
 The user may voluntarily send correspondence through their mail provider;
 support correspondence must be reflected in the public policy as applicable.
-Public endpoints could not be verified from this cloud on9November: HTTP403,
 sampled body error1010. Confirm deployment/content from a normal public browser.
 This inventory is a draft for truthful Console answers, not submitted form data.


## Policy closure update

Usage is now optional and default-off with versioned opt-in; old mandatory state
is not permission. Startup agreement does not enable it. The English policy now
explicitly includes Season/Career records, local fictional purchases, feedback and
English default. Deploy the matching public renderer/config before submission.
Owner confirms clubs are fictional; do not claim official licensing.
