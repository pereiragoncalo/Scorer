# Public leaderboard acceptance —9November2026

Result: **Season service partially verified live; Career v4 deployment missing.**
The existing safe installer is ready and its actual bundled payload passed an
isolated upgrade rehearsal. This environment has no configured SSH or real admin
credential. Owner currently cannot access bastion. Do not mark live v4 deployment
or human operator readiness complete.

## Live read-only evidence

Requests used the app's actual Scorer User-Agent, with verified HTTPS, no redirect
following and no private authentication. Earlier generic browser/Python403s do
not establish that the actual game requests are blocked.

- /health:200, ok:true.
- /v3/records?edition=world&country=Portugal&division=1:200/schema3.
- /v4/records with the same scope:404/JSON not_found.
- /v1/moderation without credentials:404, no private queue exposed.

## Own disposable live fixture

Created only a zero-goal, clearly labelled QA pending Season record under a new
random256bit write credential. No existing user records were approved, edited or
withdrawn. No usage counters were sent. Recovery credentials were held in a0600
file outside the repo, never printed, committed or uploaded. The recovery file
was deleted only after cleanup204 for both owner and reporter.

Observed live:

1. Own withdrawal supported before creating a fixture.
2. Submission without community terms rejected400.
3. Valid submission accepted204 and not publicly visible before approval.
4. Reporting that fixture accepted204; invalid reason rejected400.
5. Own withdrawal accepted204 and own fixture absent from the public board.
6. Repeated withdrawal accepted204 on the paced repeat.
7. After withdrawal, reporting the removed publisher rejected400.
8. Both fixture/reporter identities cleaned with204; no recovery credentials remain.

The initial run observed one503 on repeated withdrawal. Cleanup immediately
returned204 for both credentials. A second complete run with250ms between
requests passed. The503 cause was not established; do not silently treat it as a
code bug, a security block, or proof of reliable operation under load. Preserve
both evidence files. Public absence alone cannot prove the private report row was
removed; live admin/database inspection remains unavailable. The local rehearsal
below checks those rows directly.

No live admin approval, rejection, ban or queue review was performed. Live
pre-publication invisibility plus report acceptance does not establish ongoing
human moderation.

## Actual isolated installer rehearsal

`python3 tools/play/verify_server_upgrade.py --report REPORT.json`

Starts the real pre-v4 service from qa-0.9.33 in a temporary directory/SQLite DB,
creates an approved unrelated fixture and aggregate baseline, then applies the
exact standalone Scorer-Play-Policy-0.9.40.py payload through its transactional
installer callbacks. Both service processes listen only on random loopback ports.
No systemd, SSH or public writes are involved in this rehearsal.

20checks passed: old v3/no career table; actual installer/public pages/v3/v4
verification; existing approved season record preserved; career table added;
terms enforced; both categories pending; unauthorized approval rejected; private
queue lists both without raw credentials; approval; client blocking and reload;
report visibility; bans and rejected new posts; withdrawal of both categories and
reports; unrelated records and aggregate totals preserved; no remaining career rows.

All temporary processes/databases were cleaned. Production installer rollback and
symlink tests are separate and also pass. This verifies the installer/code, not
its execution on bastion.

## Remaining deployment action

Use the already verified owner-run installer:
https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.40/Scorer-Play-Policy-0.9.40.py

When bastion access is available, run --check then the installer as root. Recheck
live /v4/records returns200/schema4 and exercise both categories with the real
moderator. The GitHub Pages final policy is already live and independent of this
service; there is no need to undo that hosting change.

Until then, keep this point open and continue independent Android acceptance.
