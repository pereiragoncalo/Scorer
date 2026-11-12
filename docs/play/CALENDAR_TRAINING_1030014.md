# World1.0 / 1030014 — calendar, training and accessible finishing

Owner confirms two legs in SAME opponent order, reversed venues, maxTWOconsecutive
home/away league fixtures for all teams. Frozen v3orientations cover2–64teams except4;
all actual regular10–24and split-group6+sizes supported. Four-team compact mirrored
round robins cannot meet max2, so that unused regular size retains the legacy
balanced fallback. No runtime solver or RNG. Existing official3/4leg/split structures
are retained; mirrored ordering applies within their phases. New seasons usev3.
Old seasons upgrade ONLY if every played fixture has the same opponent and venue;
otherwise keep the entire old schedule until rollover. First2v2rounds match across
all current regular sizes. Saved fixture identity has a frozen regression digest.

Finishing: normal aim*.75/time*1.6, header*.78/*1.6 plus close-header benefit;
penalty*.50/*2.6 and duel*.65/*2.0; stronger keeper-only reaction/read help. Previous
penalty8%/clear8–28%mix and placed-shot help retained. No launch/target/collision changes.
Paired480exact-corner shots compare13to14: long-shot goals tier1 10→15/30, tier4 9→16/30;
close headers/penalties/duels already convert almost all exact targets. Human benefit
also comes from slower aim/more time; exact-target samples are not human conversion.

Training is a no-scroll locker-room screen with an original illustrated room and
same-character seated portrait, kit palette rendered by a small shader. Start/resume/
complete/coach gate and XP/energy/morale preserved,48dp controls. Three actual screen
sizes inspected; native layout/font bounds across4languages pass. Atomic save-failure
regression confirms no training consumption. Initial generic FloatLayout composition
failed visual inspection despite valid bounds; replaced by standard BoxLayout. A
mock-save fixture initially omitted the real error message; corrected to exercise
actual os.replace failure and passed.117core cases plus measured native checks pass.

## 1. Upload to internal testing from existing bastion (root)

```bash
(
set -eu
scorer_release=$(mktemp -d /root/scorer-release.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/play-automation-v1.13/bastion_play_internal.py -o "$scorer_release/uploader.py"
printf '%s  %s\n' e1e17204aea11e69d5a68fc9b4f6a8789f472218996a070286d6ec9ae5f7f401 "$scorer_release/uploader.py" | sha256sum -c -
install -m700 "$scorer_release/uploader.py" /root/scorer-signing/play-internal.py
python3 /root/scorer-signing/play-internal.py --publish
)
```

Existing Google account/upload key reused. Confirm Committed INTERNAL version1030014.

Keep the owner unblocked while confirming Play delivery. After successful publish:

```bash
python3 /opt/scorer/server/version_updates.py --minimum 0 --latest 1030014 --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Confirm the app footer reads v1.0 (1030014), then check training chairs. The Console
release label alone does not confirm installation. Do not uninstall or clear game data.

## 2. Required update policy, after confirmed Play availability

When1030014is available to every intended player, run on bastion:

```bash
python3 /opt/scorer/server/version_updates.py \
  --minimum 1030014 \
  --latest 1030014 \
  --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Verify both minimum_version_code and latest_version_code are1030014. Reopen the
older game online, update from Play and check v1.0 (1030014), seated match fans and empty training chairs on the phone. Do not
require an internal-only build for players without internal access. Publisher
prints this activation reminder but never raises the minimum before availability.
Owner signing, live internal submission/policy activation and phone smoke require
owner execution; publishing GitHub attachments does not complete those actions.
