# Data Safety inventory — ad-free0.6.43, draft for owner review

Assess com.clemir.striker and com.clemir.scorerworld separately. Windows is not a
Play listing. Do not copy legacy single-app purchase or advertising declarations.

| Flow | Actual current treatment | Declaration considerations |
| --- | --- | --- |
| Offline careers, language, editor/SAF, fixtures | Private device files; no whole-career upload | Explain local storage, uninstall and exports |
| Optional usage, all three editions | OFF until Privacy consent;9fixed numeric counts, HTTPS stats.clemir.com/v1/usage | App interactions/selected error counters, analytics purpose, optional collection; no unique-users claim |
| Usage collector | Combined UTC-day counters90days; no raw requests/player/device/session IDs stored by own collector | Hosting/CDN necessarily process transport/IP; Cloudflare must be disclosed; inspect actual provider logs |
| Optional completed-season leaderboard | Separate explicit consent_version2; chosen name, finishing team, completed season, matches, goals, country/division; random private ownership token sent only for own records/deletion | Public profile/name/gameplay/identifier handling requires accurate disclosure; chosen name can be personal data; NOT an anonymous-only app |
| Ranking retention/removal | Best record until withdrawal; removal button erases own v1/v2 public records; offline request remains pending | Describe removal and operational support; verify public server v2 deployed before release |
| Advertising/billing | No ad SDK/UMP/native bridges, ads, rewarded buttons or stadium promotions; no billing SDK/in-app purchase | Contains ads: No, for VERIFIED ad-free artifact; do not claim AdMob collection in this release |

Both apps still use Internet for optional ranking/usage; removing advertising does
NOT make the app "collects no data". Separate consent does not excuse declaration.
Use the actual current Play form definitions for collected/shared, ephemeral
processing, optional data and service-provider transfers. Public posting is
user-directed, but its collection/storage/disclosure still needs truthful answers.
There is no SCORER email/password account or automatic save-cloud upload. Check
whether Play treats the optional persistent public identity as account creation;
do not dismiss deletion requirements solely because no password is used.

No automatic SMTP/email summaries active. Public privacy-policy URL, owner identity
and support contact remain absent from release/play.example.json; production
validation blocks them. This document is not submitted Data Safety or approval.
