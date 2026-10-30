#!/bin/bash
# Run with sudo from a reviewed checkout. Never prints administrator credentials.
set -euo pipefail
if [ "$(id -u)" != 0 ]; then echo 'Run this installer with sudo.' >&2; exit 1; fi
scorer_install_source="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for scorer_command in python3 systemctl install useradd; do command -v "$scorer_command" >/dev/null; done
if ! id scorer >/dev/null 2>&1; then useradd --system --home /var/lib/scorer --shell /usr/sbin/nologin scorer; fi
install -d -m 755 /opt/scorer /opt/scorer/server
install -d -m 700 -o scorer -g scorer /var/lib/scorer
install -d -m 700 /etc/scorer
if [ -f /var/lib/scorer/online.sqlite ]; then
    python3 - <<'PY'
import sqlite3
with sqlite3.connect('/var/lib/scorer/online.sqlite') as src,sqlite3.connect('/var/lib/scorer/online.backup.sqlite') as dst:src.backup(dst)
PY
    chmod 600 /var/lib/scorer/online.backup.sqlite
fi
install -m 644 "$scorer_install_source/anonymous_stats.py" /opt/scorer/
for scorer_file in usage_collector.py leaderboard.py dashboard.html; do install -m 644 "$scorer_install_source/server/$scorer_file" /opt/scorer/server/; done
if [ ! -f /etc/scorer/online.env ]; then
    python3 - <<'PY'
import os,secrets
fd=os.open('/etc/scorer/online.env',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'w') as f:f.write('SCORER_STATS_ADMIN_TOKEN='+secrets.token_hex(32)+'\n')
PY
fi
install -m 644 "$scorer_install_source/server/scorer-online.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable scorer-online
systemctl restart scorer-online
for scorer_attempt in 1 2 3 4 5; do
    if python3 -c 'import urllib.request; assert urllib.request.urlopen("http://127.0.0.1:8787/health",timeout=2).status==200' 2>/dev/null; then
        echo 'Scorer service ready on 127.0.0.1:8787. Configure the existing Cloudflare Tunnel public hostname to this service.'
        exit 0
    fi
    sleep 1
done
echo 'Local health check failed. Inspect: sudo systemctl status scorer-online' >&2
exit 1
