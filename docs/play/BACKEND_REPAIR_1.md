# Repair1 — complete standalone backend payload

The previous installer omitted server/privacy_cases.py and privacy_requests.py.
Bastion failed its startup import, and rollback restart was also rate-limited.
The previous successful rehearsal used a complete old source tree; it did not
validate a partially installed server. Do not rerun that old installer to fix this.

Repair1 ships the full startup closure and admin HTML, not only changed v4 files.
It tests isolated imports, disposable Collector startup/DB initialization and policy
rendering before stopping the actual service. It resets the systemd failure limit
before start and reports both original and rollback errors if recovery fails.

Verified: standalone --check;22isolated recovery/migration/protocol checks from
qa-0.9.33 with both privacy dependencies deliberately removed;6installer tests.
Existing season records and aggregate totals survive; terms/moderation/ban/block/
withdrawal work after repair. This is not remote proof or a Python3.13 execution;
local verification uses Python3.12, the owner's journal reports3.13.

Deploy the pinned standalone Scorer-Backend-Repair-1.py as root on bastion after
checking its SHA256. It targets /opt/scorer/scorer-online/local8787, preserving
existing service configuration, environment credentials, database, Tunnel and timer.
The app remains0.9.42. Actual service/public v4 verification remains pending until
owner execution. Private tokens must not be pasted into chat or committed.
