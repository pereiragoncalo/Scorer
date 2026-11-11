# Scorer World 1.0 / 1030004 — required updates

Android production checks a fixed HTTPS minimum-version endpoint on startup,
resume and periodically in menus. It compares the installed numeric version code.
The non-dismissable gate blocks gameplay and opens the official Play listing.
It never downloads an APK. No advertising or billing SDK was added.

Offline: allow play unless a previously validated cached policy requires a newer
version. A failed request cannot erase that known requirement. The private cache
is separate from career saves. Clearing app data/reinstalling clears the cache;
this is a compatibility aid, not an anti-tamper or server-access security control.
A five-second watchdog permits offline startup when no requirement is known.

Existing 1030003 has no gate: players must install 1030004 once through Play.
Play controls update availability, account eligibility and rollout timing. The
button does not force Android to install or bypass Play. Cancel leaves play blocked.

## Owner installation on bastion

The release attachment contains the full transactional backend installer. It
preflights imports, preserves existing public configuration and operator minimum,
SQLite, keys and tokens, and rolls back delivered files if restart/check fails.
The publisher uses the already installed upload key and Google service account.
Run the following as root; no credential setup is repeated:

```bash
(
set -eu
scorer_update=$(mktemp -d /root/scorer-update.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/world-1.0-1030004/Scorer-Version-Gate-Backend.py -o "$scorer_update/backend.py"
printf '%s  %s\n' 5027c24d4f79309785ca9a8510a48dfc8011d45710c9a67b04dd619b5c66ab0a "$scorer_update/backend.py" | sha256sum -c -
python3 "$scorer_update/backend.py"
curl -f https://stats.clemir.com/v1/app-version
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/play-automation-v1.2/bastion_play_internal.py -o "$scorer_update/uploader.py"
printf '%s  %s\n' e31c71b2fc4c4499584ba69e223c710b532fe7a3f492510f8fb8200c3e8e8719 "$scorer_update/uploader.py" | sha256sum -c -
install -m700 "$scorer_update/uploader.py" /root/scorer-signing/play-internal.py
python3 /root/scorer-signing/play-internal.py --publish
)
```

## Future minimum changes

Publishing a bundle does **not** raise the minimum automatically. Only after the
new version is available to **all intended players** should the operator set its
minimum. For example, after 1030005 is fully available:

```bash
python3 /opt/scorer/server/version_updates.py --minimum 1030005 --latest 1030005 --name 1.0
```

Changes take effect without restart, on each client's next successful check.
Lowering minimum to 0 revokes a mistaken requirement when clients reconnect.
Do not require a version available only to internal testers for production users.
The initial minimum/latest is 1030004 and blocks no installed gate-capable build.

## Verification

25 core release/update/backend tests pass; 8 native Kivy update/creation tests
pass, including phone sizes, actual Update touch and offline cache behavior.
Publisher has 24 fixture tests (real-artifact fixture checked separately).
AAB validated with bundletool, compiled production/World metadata, 118 native
ELF alignment checks and 16 KiB APK ZIP alignment. No owner signing, live backend
installation or Play submission was performed from this cloud workspace.
Canonical public privacy disclosure deployed and verified on GitHub Pages.
