# Sign local-name World1.0/code1030002

Asroot on owner bastion, reuse EXISTING upload identity:

```bash
(
set -eu
scorer_dir=$(mktemp -d /root/scorer-1030002.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/world-1.0-1030002/bastion_bundle_1030002.py -o "$scorer_dir/sign.py"
printf '%s  %s\n' 42f755e3c785cc2bd4b06d23c9449552c162bfc9b4a9f5c9e71e48ef92503f6e "$scorer_dir/sign.py" | sha256sum -c -
TMPDIR="$scorer_dir" python3 "$scorer_dir/sign.py"
)
```

Fresh/root directory avoids owner-observed permission error overwriting/tmpfile.
Coordinator pins input AAB2e30020eef7ddf264839221bc6ec74364908fc08490a40ed3c687aa814d8cd53
and unchanged signer5492d1fa8de0e3072960a0c34eaf05548cdaaa51c84f154d8ef579c885fa6761.
Existing/root/scorer-signing/scorer-upload.p12, alias scorer-upload. Originalpublic
certificate2259de229b49bb40e158d3c015fe1e0d2426becb4e1a4f110dbcd183b51e59a0.
Hidden existing password, no key creation/replacement or remote credential upload.

Output:/home/clemir/Scorer-World-1.0-1030002.aab. Transfer as before, create NEW
internal Play release, retain only1030002. Samepackage/app/signingidentity/testers.
Install/update from Play, inspect Portuguese club labels and centred YOUR SEASON;
physical acceptance not inferred from static/desktop render tests.
