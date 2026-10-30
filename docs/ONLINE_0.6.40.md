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
