# Scorer World 1.0 (1030035)

Player stats shows a collective-title count with a touch control opening the
complete saved trophy history (season, competition, team). Individual scoring
awards, reserve and playoff awards are excluded. Main player stats remains one
screen, with editable name/portrait/contracts unchanged. Nine languages.

The division leaderboard previously retained seasons in its database but hid all
except each publisher's best. It now lists every consented published season in
score order, retaining the existing top100 per division. Same-season retries stay
idempotent; identical names/scores in different seasons remain separate entries.
Public display remains name/goals only; moderation/block/withdrawal stay effective.
The single-file backend repair changes server/division_records.py only, backs up
known source, checks HTTP health and restores on failure. No DB migration, erasure,
new consent or republishing required for seasons already retained in the database.
Existing game clients can show the corrected list without installing1030035.

Validation:54pure/HTTP/honours/installer/publisher tests (one hostJDK skip),5native
player-layout/title-history/training tests pass. Native screenshots reviewed.
Physical Android acceptance and actual Play availability remain owner-side.
Keep minimum1030032 until Play offers this update. Commands: docs/play/FIXES_1030035.md.
