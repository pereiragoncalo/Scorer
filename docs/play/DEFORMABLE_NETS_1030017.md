# World 1.0 / 1030017 — deformable Scorer 1 nets

Corrected candidate superseding1030016: conforming box panels and floating-point seam welding; dynamic seam sweeps pass mobile/full and Windows dimensions.

Shared welded Verlet/spring cloth and cached Kivy meshes for the game and a
standalone development lab. Gravity-loaded rest slack, damping, stretch bounds,
fixed1/120step, mobile resolution and sleeping. Seven lab presets, repeat/angles/
force/all8parameters,25/50/100%,pause/step,A/B/JSON and frame/video export. Lab is
excluded from production. Square/hexagon and veil/box retained by stadium.

Post-goal presentation only: original ball/net collision, goal-line decisions,
shot trajectories, results and career unchanged. Exact legacy lateral projection
retained.59pure +30native cases passed;20paired trajectories/40shots identical
with the presentation enabled/disabled. Real Kivy simulator controls and visual
frame sequences inspected, normal and25%videos generated. Mobile CPU reference
~1.2–1.3ms/step on Linux x86_64, NOT a phone FPS claim. Native Windows/phone
acceptance pending. Original248frames/35sheets unchanged. See ../DEFORMABLE_NETS.md
for architecture, parameters, run/test commands, visual artifacts and limitations.

## 1. Upload to internal testing from existing bastion (root)

```bash
(
set -eu
scorer_release=$(mktemp -d /root/scorer-release.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/play-automation-v1.16/bastion_play_internal.py -o "$scorer_release/uploader.py"
printf '%s  %s\n' aea38ed31ac5e385d2f7a7a5e8f0239d74b27dbbf13cba469d7e996de926fedd "$scorer_release/uploader.py" | sha256sum -c -
install -m700 "$scorer_release/uploader.py" /root/scorer-signing/play-internal.py
python3 /root/scorer-signing/play-internal.py --publish
)
```

Existing Google account/upload key reused. Confirm Committed INTERNAL version1030017.

Keep the owner unblocked while confirming Play delivery. After successful publish:

```bash
python3 /opt/scorer/server/version_updates.py --minimum 0 --latest 1030017 --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Confirm the app footer reads v1.0 (1030017), then check the near-post net pocket and recovery. The Console
release label alone does not confirm installation. Do not uninstall or clear game data.

## 2. Required update policy, after confirmed Play availability

When1030017is available to every intended player, run on bastion:

```bash
python3 /opt/scorer/server/version_updates.py \
  --minimum 1030017 \
  --latest 1030017 \
  --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Verify both minimum_version_code and latest_version_code are1030017. Reopen the
older game online, update from Play and check v1.0 (1030017), seated match fans and empty training chairs on the phone. Do not
require an internal-only build for players without internal access. Publisher
prints this activation reminder but never raises the minimum before availability.
Owner signing, live internal submission/policy activation and phone smoke require
owner execution; publishing GitHub attachments does not complete those actions.
