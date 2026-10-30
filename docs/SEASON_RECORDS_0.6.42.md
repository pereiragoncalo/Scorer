# Scorer0.6.42 completed-season records

Owner screenshot showed CompactTable inside a generic auto-height scrolling
GridLayout: the table's adaptive controls overpainted the card buttons. New
SeasonRecordsScreen uses separate constrained action/table regions and paging,
no nested scroll. Responsive compact headers preserve table space; actual Kivy
layout tests compare button/table/row bounds at640x360,1280x591/density1.64,
320x240 and1366x697. Header uses actual game logo. Long prose/aliases removed.

Snapshots are captured BEFORE promotion/relegation, counter reset and season
increment. Public fields: chosen player name, finishing team (display name), total
club-season goals (league and domestic cup, as existing career total), completed
season, matches, country and finishing division. Training/international goals
are excluded by the existing club-goal counter. Mid-season transfer record uses
the team/division at season finish, with that player's whole club-season total.
No live/in-progress season totals submitted. No reconstruction of unknown old
seasons or rebranding old live alias rows as completed records.

Career stores the best completed snapshot per country/division; lower/equal goal
seasons do not overwrite it. Saved/reloaded atomically with normal career, default
empty on old saves. No RNG, simulation, promotions or fixture changes; no career
reset. World opens current country/division only; promotion publishes old tier's
finished record and shows new tier's own board. Same division number in another
country is separate. Free uses one Scorer board across Android/Windows. Server
keeps one personal best per credential/scope, tie order deterministic. Records
remain until withdrawal, not the old90day live-score expiry.

Existing alias-sharing permission does NOT authorize publishing a name/team.
consent_version2 requires new explicit Share confirmation naming the player and
fields. Usage statistics remain separate/unchanged. Stop Sharing removes v1 and
v2 entries; offline removal stays pending. Offline season records remain in career;
up to8new best snapshots uploaded per sync, acknowledged payload hashes persist.
Records are client-reported, not anti-cheat verified; no prizes/payments claim.

Backend adds /v2/records POST and GET with explicit edition,country,division query,
and /v2/records/withdraw. SQLite additive migration creates season_records table
and preserves old leaderboard/aggregate stats; v1 stays compatible with0.6.41.
Parameterized queries, bounded Unicode names/teams/control-character rejection,
strict integers, authenticated random owner credential, no identity in public
rows. New client rejects wrong-scope responses and shows Server update required
on old server404. No fallback to misleading old live scores.

IMPORTANT: laptop server upgrade REQUIRED. No SSH/root access to bastion exists
in this executor. Installer now copies shared season_records.py validator and
server/season_records.py handler; existing SQLite backup, admin secret, service
port8787 and tunnel retained. No Cloudflare/DNS change needed. New server source
must be checked out, then its installer run as root on bastion. Merely upgrading
APKs/EXE does not upgrade that server. Local migration/HTTP tests are not a live
public-v2 deployment claim. Existing usage endpoint works unchanged throughout.

Operator Codex laptop task: fetch origin/main in /home/clemir/scorer-deploy,
prepare a new detached worktree without overwriting local edits, validate installer,
and provide the absolute bash command for user's normal root SSH terminal.
After install: /health OK, v1 still responds, v2 filter query returns schema2,
private totals still deny unauthenticated requests. Test a temporary completed
record and withdraw it; no fake record retained. Do not disclose admin/tunnel
credentials. Source tests are synthetic and never post records to live server.

Release tests/artifacts recorded after validation. Next: owner update server,
upgrade app in place, Load Game, choose Share if desired, complete season; confirm
name/team/personal-best and correct division. Human Android device test pending.

Validation:174core/security +98Kivy PASS; focused4UI tests repeated after final
row-anchor fix.272unique tests, plus6native staging checks. Initial save-migration
test wrongly looked for top-level record field; corrected to existing career
envelope, full suite PASS. Actual native screenshot revealed sparse rows at
bottom; flexible spacer below rows fixed top alignment, new bound assertion
passes phone sizes. Native final run41132392263/source4339c88 built/runs actual
EXE and renders records.png using synthetic3row fixture without network posting,
asserts table/actions do not overlap and chosen name survives display. Screenshot
visually inspected. Earlier native artifact discarded before delivery.

Both final Android packages truly rebuilt after row fix; old upgrade signature,
ZIP16KB and118ELF LOAD16KB PASS. Compiled bytecode inspected with matching3.14:
Widget spacer, pre-reset snapshot/keep_best and consent_version2 present. Initial
checker assumed integer2 was always in co_consts; updated for Python3.14
LOAD_SMALL_INT opcode, no application change needed. Actual native archive
validates fixed Free/no server/keys/saves/SDK/billing, public HTTPS endpoints and
CA content. Human Android device/full-match test not claimed.

Latest cloud-executor public v2 probe was404; server upgrade is pending owner
execution on bastion. No claim of deployed public v2 or remote completed records
yet. Existing usage/v1 preserved; apply installer from new checkout, not old0.6.41.

[Scorer-Free-0.6.42.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.42/Scorer-Free-0.6.42.apk)

[Scorer-World-0.6.42.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.42/Scorer-World-0.6.42.apk)

[Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.42/Scorer-Free.exe)
