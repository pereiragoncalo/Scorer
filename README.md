# Scorer0.6.40 QA candidates

# Scorer0.6.40: aim consistency and optional own-hosted online service

Shared original Kivy engine: remove hidden random aim offset; launch solver
matches fixed-step gravity and0.996 drag. Visible marker sits exactly on goal
plane. No collision/result bypass: blockers, keeper, frame and floor still count.
Paired tests cover30 crossed shots from x=-12,-6,0,6,12 at three goal targets,
both geometry profiles, actual engine line intersection within1e-5m. Aim outside
mouth can still miss. The previous random spread was intentional accuracy noise;
owner request now makes the visible marker authoritative for unimpeded shots.
Training retains stand mesh but omits crowd on every platform, games unchanged.
Windows fixed build starts fullscreen auto; Android config untouched.

Optional GLOBAL action inside Top Scorers for both editions; separate Free/World
ranking labels, season/matches/goals and random pseudonym (never career name).
Explicit join independent of usage consent; background submissions after completed
matches; server public top100; withdraw removes all own entries, failed removal
remains pending and can retry via Refresh. HTTPS only, no redirects,5s timeout,
bounded response/payload, parameterized SQLite,20requests/sec/16connections,
server hashed high-entropy random credential, no raw request/IP logs. Private
/admin page asks for server bearer token; credentials never in app. Existing
Free opt-in aggregate usage counters /v1/usage and authenticated /v1/totals retained.
World remains no-op for usage stats, now optional leaderboard transport with
INTERNET/ACCESS_NETWORK_STATE permissions. No Google ad SDK added to World.

Scores are SELF-REPORTED and forgeable by modified clients; validation is not
anti-cheat. No verified prizes/competitive integrity claim. Joining publishes
only displayed random alias/edition/season/matches/goals. SQLite has90day write-
triggered cleanup; stable hostname portable to Linux cloud. Existing data path
and careers unchanged. No account/login/payment or extra dependencies added.

Deployment: server/ONLINE_SETUP.md, systemd service127.0.0.1:8787 and existing
Cloudflare Tunnel preferred, so router/staticWAN IP unnecessary. Public example
stats.clemir.com is a proposal, not an existing configured destination. TLS edge
provider must be disclosed before activation. All candidate configs remain empty:
no laptop access/tunnel/DNS destination supplied and NO online upload/service
activation. Local backend tests do not prove Internet reachability. Website
stays untouched. Caddy optional direct443 deployment example and Docker copy list
updated; no Docker backend image actually built in this stage.

Test results/artifact checks recorded after native build. Native Windows source
smoke verifies fullscreen; source Kivy covers offline screen/consent, real local
HTTP tests cover submit/read/delete and protected totals. No Android physical
device/full human match or live external server test claimed. Next: owner laptop
install/public HTTPS checks, configure destination, fresh privacy disclosures,
rebuild/test actual upload before calling leaderboard live.

## Verified artifacts

166core/security +96Kivy tests PASS. Added30real engine crossed-shot cases inside
one regression.5actual local HTTP/client tests,2Kivy online UI cases included.
Windows native run41115421830/sourcef688333 PASS:6staging checks, real frozen
career/training/automated engine match/save-reload/close, fullscreen true,
1024x768hub/goal/empty-training FBO renders. Human full-match still owner test.
Android Free/World0.6.40 code1026640 both actually compiled; signatures preserve
prior debug certificate, ZIP16KB and118ELF LOAD16KB checks PASS. World verifier
initially assumed a single bool constant; fixed to verify named WORLD_BUILD and
WORLD_PREVIEW assignments instead. No APK binary change required for verifier fix.
Existing source regression expecting random target dispersion now asserts fixed
marker target, bounded compensated speed and original training distances. Initial
run failed obsolete expectation; final complete suite passes. No failures hidden.

Static training screenshot reuses final smoke state SHOT4/3; it is a render fixture,
not a playable fourth shot. Existing careers/WIP retained; no release signing/Play
store activation, remote destination or human Android device testing claimed.

[Scorer-Free-0.6.40.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.40/Scorer-Free-0.6.40.apk)

[Scorer-World-0.6.40.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.40/Scorer-World-0.6.40.apk)

[Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.40/Scorer-Free.exe)

Save and Exit first, replace Windows EXE/upgrade same Android app, then Load Game; keep saved-career folders. Android debug and Windows unsigned; not Play Store release.
