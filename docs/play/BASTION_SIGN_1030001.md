# Sign corrected1.0/code1030001 on owner bastion

Run as root after verified public attachment delivery:

```bash
(
set -eu
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/world-1.0-1030001/bastion_bundle_1030001.py -o /tmp/scorer-1030001.py
printf '%s  %s\n' f378c524f2376eccd11b770b289373874fc2aee6143b7a5974f1d113cbb3e509 /tmp/scorer-1030001.py | sha256sum -c -
python3 /tmp/scorer-1030001.py
)
```

Downloads and verifies AAB e0dda65b3f97ca2ff684595be8b31f7870cf070d3bb20449290823b12774eabc
and unchanged signing helper5492d1fa8de0e3072960a0c34eaf05548cdaaa51c84f154d8ef579c885fa6761.
Reuses/root/scorer-signing/scorer-upload.p12, verifies original public certificate
2259de229b49bb40e158d3c015fe1e0d2426becb4e1a4f110dbcd183b51e59a0,
requests existing password with hidden getpass. Refuses existing output.
No key generation, credential sharing or Play upload.

Output:/home/clemir/Scorer-World-1.0-1030001.aab. Transfer this new signed file to
phone/Drive using same method as before. Create a NEW internal test release;
include only1030001, remove retained1030000 if shown. Keep same app/package,
Google Play App Signing and upload identity. Test phone installation and new
career creation before production promotion. Do not uninstall existing saves
merely to update a Play-signed build. Track suspension remains owner action.
