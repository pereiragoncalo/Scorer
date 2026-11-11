# Sign city/colour1.0/code1030003

Run asroot on owner bastion with existing upload key:

```bash
(
set -eu
scorer_dir=$(mktemp -d /root/scorer-1030003.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/world-1.0-1030003/bastion_bundle_1030003.py -o "$scorer_dir/sign.py"
printf '%s  %s\n' 9960b8b6349e0b9ea68f633db5e852252f2bc85fa1caa536b5acc74e03a979a1 "$scorer_dir/sign.py" | sha256sum -c -
TMPDIR="$scorer_dir" python3 "$scorer_dir/sign.py"
)
```

Pinned unsigned AAB14a143d6f879d2bc11def5cf35d32fc5e8fe11fefb2112baf7690d26edf076bb;
unchanged signer5492d1fa8de0e3072960a0c34eaf05548cdaaa51c84f154d8ef579c885fa6761.
Reuse/root/scorer-signing/scorer-upload.p12, aliasscorer-upload. Originalpublic cert
2259de229b49bb40e158d3c015fe1e0d2426becb4e1a4f110dbcd183b51e59a0. Existing hidden
password, no key creation or remote upload. Freshroot tempdir avoids previous/tmp
permission issue. Refuses existing output, preserving any previously signed file.

Output:/home/clemir/Scorer-World-1.0-1030003.aab. Transfer tophone/Drive as before;
NEW internal release, only1030003. Same package/Play signing/testers. Verify Play
installation, city/colour names and matching kits before production promotion.
