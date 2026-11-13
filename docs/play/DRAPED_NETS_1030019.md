# World 1.0 / 1030019 — test natural resting nets in game

Run as root on the existing bastion. This reuses its private upload key and Google
service account; no replacement key or credentials belong in chat.

```bash
(
set -eu
scorer_release=$(mktemp -d /root/scorer-release.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/play-automation-v1.18/bastion_play_internal.py -o "$scorer_release/uploader.py"
printf '%s  %s\n' ec1404c13051b6faa41f7e03d81663a7a09651bc1163d8a40c29bf6ab4df5649 "$scorer_release/uploader.py" | sha256sum -c -
install -m700 "$scorer_release/uploader.py" /root/scorer-signing/play-internal.py
python3 /root/scorer-signing/play-internal.py --publish
python3 /opt/scorer/server/version_updates.py --minimum 0 --latest 1030019 --name 1.0
curl -f https://stats.clemir.com/v1/app-version
)
```

Confirm Committed INTERNAL version1030019. Update through Play without
uninstalling or clearing data. Check installed footer v1.0 (1030019), an existing
career, training and match goals with both net patterns. Check that unloaded side nets no longer bulge outward. The cloth moves broadly on impact;
the visual ball touches the side, enters the rear pocket and drops/rolls to rest.
Ground vertices stay fixed; cord pole ends remain fixed and net ends yield a
little. Physics and scores remain authoritative and separate from presentation.

## Only after confirmed Play availability to every intended player

```bash
python3 /opt/scorer/server/version_updates.py --minimum 1030019 --latest 1030019 --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Do not require this internal build for users without internal access. A Console
release label does not prove handset availability. Google Play and phone
acceptance require the owner; cloud compilation is not Play deployment.
