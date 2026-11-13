# World 1.0 / 1030020 — net variants and all pending changes

Run as root on the existing bastion. Reuses the existing upload key and Google
service account. The backend step adds the two global per-season leaderboards,
retaining old APIs and counters, with a file backup and rollback on failed checks.

```bash
(
set -eu
scorer_release=$(mktemp -d /root/scorer-release.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/world-1.0-1030020/Scorer-Season-Leaderboard-Backend-Repair-1.py -o "$scorer_release/backend.py"
printf '%s  %s\n' a63ffd36b221bd295122098fd157aa034fb8e66480c14e5206bc599d3951e94e "$scorer_release/backend.py" | sha256sum -c -
python3 "$scorer_release/backend.py"
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/world-1.0-1030020/bastion_play_internal.py -o "$scorer_release/uploader.py"
printf '%s  %s\n' d346ae5d2d10c28a9d6cf2538320dedfbcebabf61e75070562683df92479e14b "$scorer_release/uploader.py" | sha256sum -c -
install -m700 "$scorer_release/uploader.py" /root/scorer-signing/play-internal.py
python3 /root/scorer-signing/play-internal.py --publish
python3 /opt/scorer/server/version_updates.py --minimum 0 --latest 1030020 --name 1.0
curl -f https://stats.clemir.com/v1/app-version
)
```

Confirm `Committed INTERNAL version1030020`. Update from Play without uninstalling
or clearing data. Confirm installed footer `v1.0 (1030020)` before testing:

- Existing save loads; training has empty seats and both bib teams.
- Stadiums include 1.80 m box and 3.50 m triangular nets, plus both original depths,
  each square/hexagonal. Exactly three rear poles/cords, without side stanchions.
- Net moves on ball contact; a resting ball cannot inflate cloth. Turf stays fixed.
- Goal timing is less clustered. Calendar preserves played games; incompatible
  older saves change to v4 next season. At most two same-venue fixtures remain
  possible; this is not strict alternation for every club.
- At season end, the review offers publish/decline. Publish asks only for the public
  name, applying to this season alone. The Leaderboard button only reads Division
  1 or 2, pooled across countries, showing name and league goals. New names require
  moderator approval under `/admin/manage`.

Only after this exact build is offered on every intended handset/track:

```bash
python3 /opt/scorer/server/version_updates.py --minimum 1030020 --latest 1030020 --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Keep minimum zero while Google Play propagation is pending. Never require an
internal build for players who cannot access that track. Compilation and Console
labels do not establish actual handset availability.
