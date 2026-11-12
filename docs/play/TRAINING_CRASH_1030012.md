# World 1.0 / 1030012 — bounded mobile graphics batches

Owner reports a training-entry crash. Device version/club requested; no crash log
or exact device cause confirmed. Stress test found a concrete defect: maximum
supported ground creates a77400-index chair batch above Kivy's65535index COUNT
limit. Prior tests checked only the largest index value, which is insufficient.
Stand quad caches now split at24000indices; crowd at1024fans/18432indices. Keeps
all chairs, colour, seating, cheers, saves/physics/package/key and visible build code.
A maximum150000-capacity empty-training and full-attendance match regression passes.
20existing seat/stadium/celebration cases passed; initial new fixture incorrectly
assumed offers were objects, corrected to use an actual league opponent before
passing the targeted regression. This fixes the reproduced mesh limit; resolution
of the owner's specific device crash still needs handset acceptance.

## 1. Upload to internal testing from existing bastion (root)

```bash
(
set -eu
scorer_release=$(mktemp -d /root/scorer-release.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/play-automation-v1.11/bastion_play_internal.py -o "$scorer_release/uploader.py"
printf '%s  %s\n' 9c4c7c7a8f8a5ff1eb3e037cb94260645d973f80bdcf58bcbfdb553bf2876350 "$scorer_release/uploader.py" | sha256sum -c -
install -m700 "$scorer_release/uploader.py" /root/scorer-signing/play-internal.py
python3 /root/scorer-signing/play-internal.py --publish
)
```

Existing Google account/upload key reused. Confirm Committed INTERNAL version1030012.

Keep the owner unblocked while confirming Play delivery. After successful publish:

```bash
python3 /opt/scorer/server/version_updates.py --minimum 0 --latest 1030012 --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Confirm the app footer reads v1.0 (1030012), then check training chairs. The Console
release label alone does not confirm installation. Do not uninstall or clear game data.

## 2. Required update policy, after confirmed Play availability

When1030012is available to every intended player, run on bastion:

```bash
python3 /opt/scorer/server/version_updates.py \
  --minimum 1030012 \
  --latest 1030012 \
  --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Verify both minimum_version_code and latest_version_code are1030012. Reopen the
older game online, update from Play and check v1.0 (1030012), seated match fans and empty training chairs on the phone. Do not
require an internal-only build for players without internal access. Publisher
prints this activation reminder but never raises the minimum before availability.
Owner signing, live internal submission/policy activation and phone smoke require
owner execution; publishing GitHub attachments does not complete those actions.
