# World 1.0 / 1030010 — stadium seats

Permanent individual moulded stadium chairs use the HOME club primary colour in
all stands, including visitor areas. Back shells, pans, front lips and supports
follow the projected straight/curved stands and tiers; aisles stay clear.
Training uses the player's own ground with every chair visible and no spectators
or stewards. Normal match fans sit with bent knees; existing atlas bands are
posed as torso/thighs/shins by the renderer, with no new/replaced PNG assets.
Their existing team-only celebration frames rise and then return to the chairs.
Current fan scale, occupancy/allocation, saves and gameplay physics are retained.
Crowd meshes split below GLES unsigned-short index limits (at most4500fans/batch).

30native stadium/seat/celebration/attendance cases pass, including home colour on
away fixtures, own-ground empty training, chair/fan count separation, fixed chairs
through cheers and returning spectators. Actual match/training screenshots checked.
A preview fixture initially ran the Free edition; corrected to World before the
successful screenshots. The production AAB includes all1030009portrait/keeper/header
fixes. Physical Android owner playtest remains pending.

## 1. Upload to internal testing from existing bastion (root)

```bash
(
set -eu
scorer_release=$(mktemp -d /root/scorer-release.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/play-automation-v1.8/bastion_play_internal.py -o "$scorer_release/uploader.py"
printf '%s  %s\n' 1192051a22a4326ac620642396acccf9b1832834f9ccb093c4e233ebe42b1234 "$scorer_release/uploader.py" | sha256sum -c -
install -m700 "$scorer_release/uploader.py" /root/scorer-signing/play-internal.py
python3 /root/scorer-signing/play-internal.py --publish
)
```

Existing Google account/upload key reused. Confirm Committed INTERNAL version1030010.

## 2. Required update policy, after confirmed Play availability

When1030010is available to every intended player, run on bastion:

```bash
python3 /opt/scorer/server/version_updates.py \
  --minimum 1030010 \
  --latest 1030010 \
  --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Verify both minimum_version_code and latest_version_code are1030010. Reopen the
older game online, update from Play and check seated match fans and empty training chairs on the phone. Do not
require an internal-only build for players without internal access. Publisher
prints this activation reminder but never raises the minimum before availability.
Owner signing, live internal submission/policy activation and phone smoke require
owner execution; publishing GitHub attachments does not complete those actions.
