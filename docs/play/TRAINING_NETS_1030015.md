# World 1.0 / 1030015 — match training and stadium nets

Training reuses all ten match delivery kinds (cross, deep cross, corner, cutback,
first-time, rebound, free kick, long shot, through ball, penalty), including their
physical contact points and buildup. Three weekly saved attempts, rewards, focus
and no-free-retry rules retained. Heading/penalty focus influences one attempt;
other attempts use the same weighted match variety. Local world/season/week/club
seed retains the kind/contact on resume without consuming career RNG. Training
keeps its manual touch aiming and unlimited practice decision time.

Five per side counting hero/keeper: fluorescent yellow/orange sleeveless bibs over
pale training tops; original source PNGs, skin and authored joints unchanged.
Empty home-colour chairs retained. Locker-room preparation screen retained.

Each stadium has a stable home-UID choice of square/hexagon mesh and either
legacy veil with short stanchions or a rectangular box without stanchions, held
by cords to exactly three separate rear poles. Training uses the same home net.
Associations are fictional presentation choices, not verified real stadium nets.
Box swept roof/back/side collisions use the rendered dimensions; one deformation
field keeps all seams closed during overlapping ripples. Mouth/post dimensions,
launch solver and goal-line scoring unchanged. GLES2 line meshes stay below24000
indices. Previous calendar/difficulty/save fixes retained.

105 core cases passed (91 career/balance/calendar/development +14 opportunity,
training-gate and original sprite-payload checks); 20 native training/geometry/
mesh/balance checks passed, plus native actor/opportunity regressions. Kivy
screenshots inspected for four net styles; this is not handset acceptance.
Initial native cases exposed missing no-club fallback and zero-duration state
reset, corrected; historical tests expecting empty training updated to the new
explicit owner requirement. First Android attempt hit temporary disk exhaustion;
old delivery artefacts archived with their original path linked, then rebuilt.
No signing key or Google credential is received by the cloud.

## 1. Upload to internal testing from existing bastion (root)

```bash
(
set -eu
scorer_release=$(mktemp -d /root/scorer-release.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/play-automation-v1.14/bastion_play_internal.py -o "$scorer_release/uploader.py"
printf '%s  %s\n' dcfef717428c84ef9ced8bb689f6f4e6b652b45bea0c61648487c65a275d092d "$scorer_release/uploader.py" | sha256sum -c -
install -m700 "$scorer_release/uploader.py" /root/scorer-signing/play-internal.py
python3 /root/scorer-signing/play-internal.py --publish
)
```

Existing Google account/upload key reused. Confirm Committed INTERNAL version1030015.

Keep the owner unblocked while confirming Play delivery. After successful publish:

```bash
python3 /opt/scorer/server/version_updates.py --minimum 0 --latest 1030015 --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Confirm the app footer reads v1.0 (1030015), then check bib teams, deliveries and the home net. The Console
release label alone does not confirm installation. Do not uninstall or clear game data.

## 2. Required update policy, after confirmed Play availability

When1030015is available to every intended player, run on bastion:

```bash
python3 /opt/scorer/server/version_updates.py \
  --minimum 1030015 \
  --latest 1030015 \
  --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Verify both minimum_version_code and latest_version_code are1030015. Reopen the
older game online, update from Play and check v1.0 (1030015), seated match fans and empty training chairs on the phone. Do not
require an internal-only build for players without internal access. Publisher
prints this activation reminder but never raises the minimum before availability.
Owner signing, live internal submission/policy activation and phone smoke require
owner execution; publishing GitHub attachments does not complete those actions.
