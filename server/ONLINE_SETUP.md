# Laptop service, later portable to Linux cloud

Private local HTTP127.0.0.1:8787, public HTTPS443. Prefer the owner's existing
Cloudflare Tunnel; no incoming router port or static WAN IP required. Add public
hostname stats.clemir.com to that tunnel with service http://127.0.0.1:8787.
Do not alter api-social or mail/DNS records. Existing tunnel must remain running;
laptop must be on. No tunnel/DNS/remote host deployment has occurred here.

Install this repository at /opt/scorer on laptop. Create dedicated account and
private data directory (Linux administrator terminal):

```
sudo useradd --system --home /var/lib/scorer --shell /usr/sbin/nologin scorer
sudo install -d -m 700 -o scorer -g scorer /var/lib/scorer
sudo install -d -m 700 /etc/scorer
sudo sh -c 'umask 077; printf "SCORER_STATS_ADMIN_TOKEN=%s\n" "$(openssl rand -hex 32)" > /etc/scorer/online.env'
sudo install -m 644 /opt/scorer/server/scorer-online.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now scorer-online
curl --fail http://127.0.0.1:8787/health
```

Python3 standard library only. Open https://stats.clemir.com/admin; type server
administrator token to load totals. Token never belongs in game or Git. Dashboard
uses no cookies/localStorage/CDN; private aggregate GET requires bearer token.
Public leaderboard aliases/season/goals/matches are separate opt-in data. Only
hashed random player credentials stored, no raw token/IP/request-body logs. HTTPS
edge provider may process IPs; disclose provider before activating client endpoint.
Caddy/reverse proxy and tunnel request logging must be disabled. Keep laptop
firewall closed to8787; do not expose raw Python HTTP directly to internet.

GET/v1/leaderboard top100 goals descending, matches ascending; separate edition
labels and season displayed. Scores are self-reported, not anti-cheat verified.
Bounded inputs/progress checks discourage accidents, not malicious clients. No
prizes/payments/use as authoritative competition. A determined modified game can
forge results or create identities. Delete own rows via credential withdrawal;
unavailable removal remains pending locally.90day retention on accepted writes.
Stats remain optional/default-off aggregate counters, no names/sessionIDs. Not
unique players, force-kill may omit session end. Current World retains no-op usage
stats; World online feature is optional leaderboard only.

Before activating, verify public TLS/health, private totals rejection and real
submit/read/withdraw on HTTPS; configure online_config.ORIGIN and Free staging
--analytics-endpoint https://stats.clemir.com/v1/usage explicitly, rebuild/test
artifacts and update privacy disclosure. Current empty endpoint builds transmit
nothing. Changing origin clears consent. Do not claim remote collection live.

Migration: stop scorer-online, copy online.sqlite plus service/repo and private
environment config securely to new Linux host, restore ownership/mode, start it,
change the stable hostname route. Keep old host stopped to prevent split writes.
Back up SQLite via sqlite3.Connection.backup or stop service before file copy.

A reviewed checkout also includes `sudo bash server/install_online.sh` for
installation/update: dedicated user, private environment token, SQLite backup
before updates, systemd restart and loopback health check. It never prints token.
Installer syntax checked here; not executed on the owner laptop.
