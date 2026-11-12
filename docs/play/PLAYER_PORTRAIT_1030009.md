# World 1.0 / 1030009 — player portrait, keeper saves and headers

Three columns: season stats at left, career stats in the centre and a passport-style
photo of the existing player in a white T-shirt at right. Editable name, age and
monthly salary are captions under the picture. All controls fit without scrolling.

Frontal catches foreshorten forward with the ball attached to the physical gloves,
without a sideways 2D rotation. Real high central glove contacts use a new tip-over
sprite and launch the active ball above the crossbar through the existing solver.
No new collision or forced non-goal outcome. Headers pause just before the forehead
at 1.65m, then use the authored contact frame on release. Original240sprite frames
remain unchanged; new8-frame keeper clip uses the existing palette/atlas format.

14native portrait/refinement/creation cases and responsive name/photo/save checks
at three sizes pass.17keeper/header/sprite/opportunity/difficulty/portrait native
cases and11asset/opportunity cases pass. Actual staged screenshots inspected.
The first tip-over fixture used a noncentral glove position; corrected to a real
central-jump phase before the passing physical trajectory test.

## 1. Upload to internal testing from existing bastion (root)

```bash
(
set -eu
scorer_release=$(mktemp -d /root/scorer-release.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/play-automation-v1.7/bastion_play_internal.py -o "$scorer_release/uploader.py"
printf '%s  %s\n' 55d323d6b915e916111d9913d6b075289a94405a5b7c12b556eb163e5e6cbdbe "$scorer_release/uploader.py" | sha256sum -c -
install -m700 "$scorer_release/uploader.py" /root/scorer-signing/play-internal.py
python3 /root/scorer-signing/play-internal.py --publish
)
```

Existing Google account/upload key reused. Confirm Committed INTERNAL version1030009.

## 2. Required update policy, after confirmed Play availability

When1030009is available to every intended player, run on bastion:

```bash
python3 /opt/scorer/server/version_updates.py \
  --minimum 1030009 \
  --latest 1030009 \
  --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Verify both minimum_version_code and latest_version_code are1030009. Reopen the
older game online, update from Play and check portrait, catches, high tips and forehead headers on the phone. Do not
require an internal-only build for players without internal access. Publisher
prints this activation reminder but never raises the minimum before availability.
Owner signing, live internal submission/policy activation and phone smoke require
owner execution; publishing GitHub attachments does not complete those actions.
