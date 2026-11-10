# Sign the verified World1.0 AAB locally on bastion

Unsigned release candidate:
https://github.com/pereiragoncalo/Scorer/releases/download/world-1.0-unsigned/Scorer-World-1.0-unsigned.aab

116946453bytes; SHA256:
`2d44aa9197c3d97f37cad8569ed70ce1c5333882852276e7d44ef34283cc9730`.

Standalone signing helper:
https://github.com/pereiragoncalo/Scorer/releases/download/world-1.0-unsigned/sign_local_bundle.py

SHA256 `5492d1fa8de0e3072960a0c34eaf05548cdaaa51c84f154d8ef579c885fa6761`.
Both anonymous downloads were independently verified against the tested local files.

Owner key already exists at /root/scorer-signing/scorer-upload.p12, alias
scorer-upload. The public certificate fingerprint from owner terminal is:
`2259de229b49bb40e158d3c015fe1e0d2426becb4e1a4f110dbcd183b51e59a0`.
Do not generate a new key. The helper must abort on a certificate mismatch.

As root, after downloading/checking both files, run:

```sh
python3 /tmp/scorer-sign-aab.py \
  --input /tmp/scorer-world-1.0-unsigned.aab \
  --output /home/clemir/Scorer-World-1.0.aab \
  --keystore /root/scorer-signing/scorer-upload.p12 \
  --input-sha256 2d44aa9197c3d97f37cad8569ed70ce1c5333882852276e7d44ef34283cc9730 \
  --certificate-sha256 2259de229b49bb40e158d3c015fe1e0d2426becb4e1a4f110dbcd183b51e59a0
```

The password prompt is hidden. The helper passes it only to local JDK processes
through environment selectors, verifies signature and actual certificate, and
never overwrites an existing output/key. The input must still be unsigned. Local
signing does not upload anything or establish Play approval. Share only public
signed-AAB SHA256/certificate output, never password/private.p12.

The final file is /home/clemir/Scorer-World-1.0.aab, readable by clemir for SFTP to
the owner's phone. Keep private key/password backups separate before enrollment.
In Console use Play App Signing (Google-generated app signing identity separate
from upload key) and INTERNAL testing first. Complete actual forms and any account
requirements. Do not submit the unsigned source as the signed release.

Before replacing DEBUG installation with Play, export/verify the local career:
the installation signatures differ. Actual Play installation/signature-transition
recovery, pre-launch results and genuine Android screenshots remain pending.
