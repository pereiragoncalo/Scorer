# World 1.0 / 1030008 — actual stats, another10%crowd size

Player panel becomes PLAYER STATS, with SEASON STATS and CAREER STATS. Season:
club goals, best coach trust and league scorer rank. Career: one tracked club-goal
total, transfers and international appearances. No target denominators or bars.
Underlying achievements/progress, totals, name editing and saves are unchanged.
Monthly salary remains clear without /month. All9languages updated; no scrolling.

Supporter height/width are another10%above1030007: multiplier.90→.99, floor5→5.5px,
cap38.75→42.625px. Feet/atlas/aspect/seating/team colours and animations unchanged.
This is37.5%above the pre1030007size, not another25%. Players/keeper/physics unchanged.
24native player/refinement/stadium/celebration tests pass, and the actual staged
production stats screen was visually checked using the reported6goals/91trust case.

## 1. Upload to internal testing from existing bastion (root)

```bash
(
set -eu
scorer_release=$(mktemp -d /root/scorer-release.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/play-automation-v1.6/bastion_play_internal.py -o "$scorer_release/uploader.py"
printf '%s  %s\n' cfacf82863c3560b9c0032cb924f6f775a6aee69283d3facdece47e2bb33e6f9 "$scorer_release/uploader.py" | sha256sum -c -
install -m700 "$scorer_release/uploader.py" /root/scorer-signing/play-internal.py
python3 /root/scorer-signing/play-internal.py --publish
)
```

Existing Google account/upload key reused. Confirm Committed INTERNAL version1030008.

## 2. Required update policy, after confirmed Play availability

When1030008is available to every intended player, run on bastion:

```bash
python3 /opt/scorer/server/version_updates.py \
  --minimum 1030008 \
  --latest 1030008 \
  --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Verify both minimum_version_code and latest_version_code are1030008. Reopen the
older game online, update from Play and check stats/crowd on the phone. Do not
require an internal-only build for players without internal access. Publisher
prints this activation reminder but never raises the minimum before availability.
Owner signing, live internal submission/policy activation and phone smoke require
owner execution; publishing GitHub attachments does not complete those actions.
