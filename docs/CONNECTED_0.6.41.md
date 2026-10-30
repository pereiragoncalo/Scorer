# Scorer0.6.41: visible leaderboard and owner-hosted usage

LEADERBOARD is a main-menu action on Android Free, Android World and Windows
Free, including CompactHub. Normal footer has five columns (one row landscape),
with existing Play/Training alignment; no extra main-menu scroll. Existing GLOBAL
shortcut in Top Scorers retained. Public read does not require publishing scores;
join is separate explicit opt-in, random alias, no real career names; withdraw
removes all own rows and retries offline removal via Refresh. Public scores remain
self-reported and not anti-cheat verified. Free/World display separate rows.

All three builds connect to https://stats.clemir.com. Usage transport destination
https://stats.clemir.com/v1/usage; private owner page /admin (existing server
credential remains laptop-only). Statistics default OFF and independent of public
ranking; Privacy choice required. Changing from local-only resets consent/scope.
World now offers the same explicit usage choice and approved nine-event allowlist,
no Google SDK/ads/billing. No names, save files or persistent user/session IDs in
usage. Existing server protocol discriminator app=scorer_free is a historical
family constant reused for aggregate counters from all three editions; the owner
gets combined totals, NOT platform/edition breakdown or unique user counts.
No backend upgrade is required for this compatible protocol. Endpoint credentials
are not bundled. Stable hostname remains portable to future Linux cloud host.

Added verified TLS helper: certifi when installed, bundled Mozilla CA roots for
Android where certifi is absent. Public CA bundle extracted unchanged from the
previous native Windows certifi2026.10.23 package;118CA certs, no session proxy CA.
.crt included in staged assets/spec. No TLS bypass or sensitive certificate.
Scorer User-Agent explicitly used for leaderboard; initial plain urllib probe
received403 whereas app/curl requests worked; actual client HTTPS verified.

Real HTTPS test against laptop: /health OK, public ranking readable, anonymous
access to private totals404; submitted QA-Connectivity temporary entry, observed
it, withdrew it and confirmed removal. No fake entry retained. Exactly ONE
technical sessions counter was sent successfully to validate the usage receiver;
this is not a real player's session. No administrator token read or transmitted.

Core/Kivy results and actual frozen Windows/Android artifact verification follow.
No physical Android device or human complete-match test claimed. No public store,
payments, production advertising, website/DNS/tunnel change from this workspace.
The owner configured scorer-bastion tunnel on Debian bastion; clemir-social uses
its separate existing tunnel on Windows lauany, which remains untouched.

Files: shared menu and CompactHub; original game privacy action; usage factory;
public configs/staging version0.6.41/1026641; Windows frozen checks; verified TLS
module and public CAasset; tests. Save schema/path/game simulation unchanged.
Next: upgrade in place, Load Game, tap Leaderboard/Refresh, optionally Join; enable
usage independently under Privacy and check owner totals after Save and Exit.
