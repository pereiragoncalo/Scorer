# Scorer0.6.41 QA candidates

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

Validation:167core/security +97real Kivy cases PASS. Main button and independent
World usage choice covered; initial Windows layout test caught the fifth footer
button wrapping to a second row, then fixed _arrange to five columns and repeated
entire UI suite successfully. Explicit fixture patches ensure automated tests
never send fabricated traffic to the owner host. Endpoint/CA bytecode inspected
inside both actual Android packages with their matching Python3.14 interpreter.
Original Android upgrade certificate, ZIP16KB/118ELF16KB and edition checks PASS.
No human phone validation claimed. Session ends remain queued if the OS terminates
the app before asynchronous delivery; next launch can flush pending totals.

Operator: no laptop reinstall, tunnel update or server token sharing is necessary
for this compatible client release. To see usage beyond the technical test, each
player must enable Privacy -> ALLOW USAGE STATS. Public ranking viewing is separate;
join after at least one completed match to publish the random alias/score. No
advertising consent is inferred from either choice. Updating existing apps keeps
private careers; close/save Windows EXE before replacing, then Load Game.

Native Windows run41123889956/source74c07af PASS:6staging checks plus frozen
new career/training/automated engine match/save-reload/close/fullscreen, main
Leaderboard button, both configured destinations, default-off consent and rendered
1024x768hub/goal/training. Actual hub screenshot inspected, all12fixtures and
10leading scorers fit; footer is one row. Archive verifies original Free identity,
no Google SDK/billing/server/private keys/saves, public CA content matches after
normalizing Git Windows CRLF newlines; HTTPS verification still mandatory.
First native run41122999548 stalled in Python/cache setup and was cancelled after
replacement progressed; cache-free setup with5minute timeout passed. No game
change was required for that retry. This is unsigned Windows QA and debug-signed
Android QA, not a store release or human-device validation.

[Scorer-Free-0.6.41.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.41/Scorer-Free-0.6.41.apk)

[Scorer-World-0.6.41.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.41/Scorer-World-0.6.41.apk)

[Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.41/Scorer-Free.exe)

Save and Exit, replace EXE or upgrade same Android app, Load Game; preserve private career folders. Main menu LEADERBOARD reads public scores. Join optional ranking separately. Privacy -> ALLOW USAGE STATS enables aggregate usage; off by default. Owner https://stats.clemir.com/admin uses laptop-only token, never in app. No server reinstall needed.
