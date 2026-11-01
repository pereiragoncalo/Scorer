#!/bin/bash
# Run as root from a reviewed checkout. Never prints administrator credentials.
set -euo pipefail
if [ "$(id -u)" != 0 ]; then echo 'Run this installer as root (su - on the laptop).' >&2; exit 1; fi
scorer_install_source="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for scorer_command in python3 systemctl install useradd; do command -v "$scorer_command" >/dev/null; done
if ! id scorer >/dev/null 2>&1; then useradd --system --home /var/lib/scorer --shell /usr/sbin/nologin scorer; fi
install -d -m 755 /opt/scorer /opt/scorer/server
install -d -m 700 -o scorer -g scorer /var/lib/scorer
install -d -m 700 /etc/scorer
# Retire the old raw database backup: the new backup process copies totals only.
if [ -f /var/lib/scorer/online.backup.sqlite ]; then rm /var/lib/scorer/online.backup.sqlite; fi
install -m 644 "$scorer_install_source/anonymous_stats.py" "$scorer_install_source/season_records.py" "$scorer_install_source/online_safety.py" "$scorer_install_source/privacy_requests.py" /opt/scorer/
for scorer_file in usage_collector.py leaderboard.py season_records.py moderation.py privacy_cases.py maintenance.py public_pages.py configure_public.py dashboard.html; do install -m 644 "$scorer_install_source/server/$scorer_file" /opt/scorer/server/; done
if [ ! -f /etc/scorer/online.env ]; then
    python3 - <<'PY'
import os,secrets
fd=os.open('/etc/scorer/online.env',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'w') as f:f.write('SCORER_STATS_ADMIN_TOKEN='+secrets.token_hex(32)+'\n')
PY
fi
install -m 644 "$scorer_install_source/server/scorer-online.service" /etc/systemd/system/
install -m 644 "$scorer_install_source/server/scorer-maintenance.service" "$scorer_install_source/server/scorer-maintenance.timer" /etc/systemd/system/
systemctl daemon-reload
systemctl enable scorer-online
systemctl restart scorer-online
systemctl enable --now scorer-maintenance.timer
for scorer_attempt in 1 2 3 4 5; do
    if python3 -c 'import urllib.request; assert urllib.request.urlopen("http://127.0.0.1:8787/health",timeout=2).status==200' 2>/dev/null; then
        echo 'Scorer service ready on 127.0.0.1:8787. Configure the existing Cloudflare Tunnel public hostname to this service.'
        exit 0
    fi
    sleep 1
done
echo 'Local health check failed. Inspect: sudo systemctl status scorer-online' >&2
exit 1
