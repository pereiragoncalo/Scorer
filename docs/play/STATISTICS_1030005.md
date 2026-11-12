# Scorer World 1.0 / 1030005 — startup agreement restores statistics

The owner explicitly requested: I AGREE enables aggregate statistics;
I DO NOT AGREE closes the game. Startup agreement now persists enabled=True
before allowing delivery and entering the start menu. Previously it only saved
an acknowledgment, leaving the default-off collector disabled. The initial
notice describes the nine counters, recipient, connection processing and settings
stop/erase. All nine supported languages have the new disclosure.

No upload before agreement. Declining clears pending counts for this session,
blocks delivery and stops the app, including if enabled in a previous run. A
failed choice save keeps the user on the notice without sending. Settings can
stop statistics for play; agreeing on a subsequent startup enables them again.
No adult PIN is requested for startup agreement. Public-name sharing keeps its
separate adult controls and explicit sharing; agreement does not enable it.
No historic sessions are fabricated. Activity while counters were off is lost.
The app remains version name1.0 with unchanged identity, careers, physics and
update-gate offline behavior. Install1030005 through Play to receive the fix.

## Install on existing bastion (root)

This installs the corrected server disclosure and pinned internal-only publisher,
then downloads/signs/uploads the new build using existing local keys/account.
No private keys or credential files are downloaded from this release.

```bash
(
set -eu
scorer_stats=$(mktemp -d /root/scorer-stats.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/world-1.0-1030005/Scorer-Statistics-Agreement-Backend-Repair-1.py -o "$scorer_stats/backend.py"
printf '%s  %s\n' 5c8d54c88e507490eb0cce421307449d44ed691f5ed97cf8a76ae6e0e0694f22 "$scorer_stats/backend.py" | sha256sum -c -
python3 "$scorer_stats/backend.py"
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/play-automation-v1.3/bastion_play_internal.py -o "$scorer_stats/uploader.py"
printf '%s  %s\n' a8f5465690aaf7346600d210f8252a03a9044f31d7969d0e48c909f793bd7cb7 "$scorer_stats/uploader.py" | sha256sum -c -
install -m700 "$scorer_stats/uploader.py" /root/scorer-signing/play-internal.py
python3 /root/scorer-signing/play-internal.py --publish
)
```

Backend installer preserves current minimum/latest operator version, SQLite,
tokens, service keys and operator settings apart from corrected legal/children
usage disclosure fields and effective date. Complete19-file dependency preflight,
local HTTP checks and transactional rollback retained. It does not raise the
minimum to1030005 or change production/tester access. Owner execution required.

## Acceptance

35 core statistics, publication and transactional-installer tests pass.17 native
UI statistics/publication tests pass, plus4 targeted startup-choice tests with
real phone touches, save-failure handling and real local HTTP collector. The
collector integration accepts one session after agreement and clears pending
counters only on successful acknowledgment. No synthetic usage sent to live.
Publisher fixture tests and AAB audit recorded in release evidence.

After Play update: accept the notice, play with internet, wait at least10seconds,
then check https://stats.clemir.com/admin. Server dates use UTC receipt day.
Aggregate totals can contain other testers; no unique-player identifiers exist.

Repair1: original installer rejected the new policy because its HTTP assertion still required the obsolete off-by-default sentence. The repaired checker validates the actual1030005 agreement/decline disclosure. Source and shipped installer rehearsed with a real isolated HTTP service, preserved historical totals and operator minimum. No app/signing/publisher change required.
