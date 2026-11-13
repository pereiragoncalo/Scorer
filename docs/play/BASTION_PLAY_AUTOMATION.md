Current target: World 1.0 / 1030020. Existing configured owners use [the update instructions](NET_VARIANTS_1030020.md); setup below is only for a new machine.

# Bastion → Google Play internal test

Owner explicitly authorized automated download/sign/upload after successfully
manually creating the app and its first internal release. App identity stays
com.clemir.scorerworld. The program only writes the internal testing track; it
cannot select production, modify listings/testers/policy forms or change signing
keys. No real API credential is present in this workspace or GitHub.

## One-time Google setup (phone browser)

1. Create **Scorer Publishing** at https://console.cloud.google.com/projectcreate
   with **No organization** for a personal account. A quota of23remaining projects
   is informational, not an error. Select this project for following Cloud steps.
2. Enable **Google Play Android Developer API**:
   https://console.cloud.google.com/apis/library/androidpublisher.googleapis.com
3. At https://console.cloud.google.com/iam-admin/serviceaccounts choose
   **Create service account**. Name **Scorer Play Uploader**, ID
   **scorer-play-uploader**. Skip both optional project-access/user-access grants;
   no Google Cloud Owner/Editor project role is needed for this API use.
4. Copy the resulting service-account email (public, safe to share). In
   https://play.google.com/console → developer-account **Users and permissions**
   → **Invite new users**, enter that email. Under **App permissions**, select
   only **Scorer**, with **View app information (read-only)** and **Release apps
   to testing tracks**. Leave account-wide/Admin/production/financial/order/listing
   permissions unset. Invite/save. Existing test-user list remains untouched.
5. In Google Cloud, open this service account → **Keys → Add key → Create new key
   → JSON**. Download that JSON to the phone. Do not open/share its contents in
   chat or put it in GitHub/Drive/public directories. This is the Google API key,
   separate from scorer-upload.p12. The P12 stays where it already is.

Google no longer requires linking a Play developer account to a Cloud project.
Official setup: https://developers.google.com/android-publisher/getting_started
API permissions are separate from optional Google Cloud project roles.

## Install the public program (bastion root)

Use the exact verified checksum in BASTION_PLAY_AUTOMATION.sha256:

```bash
(
set -eu
scorer_setup=$(mktemp -d /root/scorer-play-api.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/play-automation-v1.19/bastion_play_internal.py -o "$scorer_setup/uploader.py"
printf '%s  %s\n' d346ae5d2d10c28a9d6cf2538320dedfbcebabf61e75070562683df92479e14b "$scorer_setup/uploader.py" | sha256sum -c -
install -m700 "$scorer_setup/uploader.py" /root/scorer-signing/play-internal.py
python3 /root/scorer-signing/play-internal.py --setup-folder
)
```

The real user-facing installation command includes sha256sum -c using the pinned
hash. --setup-folder creates a random private0700directory in/home/clemir, owned
byclemir, for Termius SFTP upload. This avoids trying to upload by SFTP directly
into/root and avoids an exposed JSON copy in a publicly traversable home folder.

## Install the private Google credential once

Upload the downloaded JSON with Termius SFTP into the exact private folder printed
by --setup-folder. On bastion root, replace the example path with that file:

```bash
python3 /root/scorer-signing/play-internal.py --install-credentials /home/clemir/scorer-play-setup-EXAMPLE/downloaded-key.json
python3 /root/scorer-signing/play-internal.py --check
```

The program validates type/Google endpoint/email shape, copies exclusively to
/root/scorer-signing/google-play-service-account.json mode0600, refuses a different
existing credential, and preserves the upload keystore. Identical reinstall is
idempotent. Source remains in its private folder; remove only that source copy
after confirming setup. Do not send private files/passwords/access tokens here.
--check gets an OAuth token, creates/reads/deletes its own temporary edit, prints
internal version codes, and neither uploads a bundle nor commits a release.

## Automatic approved internal release

```bash
python3 /root/scorer-signing/play-internal.py --publish
```

For the approved1.0/code1030003 candidate it downloads/verifies/signs if the signed
file is absent, asks for the existing P12 password locally, then verifies:
- exact approved ZIP payload digest, retaining arbitrary compression/signing time;
- valid JAR signature and original owner upload certificate;
- API-reported versionCode1030003 and signed file SHA256.

It uploads in8MiB resumable chunks (256KiBmultiple), queries server offset after
lost acknowledgments, then sets only internal to the new completed release,
validates the temporary edit, and commits. Old internal bundle codes are excluded;
no production/listing/tester/API-permission endpoints are called. Newer internal
versions cannot be downgraded; identical already-completed uploads are no-ops;
existing version with another hash stops. Both --check/--publish hold the same
local lock. Errors before commit clean only this program's edit. Uncertain commit
responses are not blindly retried or reported as definitely unpublished.

Owner's first real upload/validation succeeded, but Google rejected the final commit:
"Changes are sent for review automatically. The query parameter changesNotSentForReview
must not be set." Version1.1 therefore omits that incompatible parameter. Commit
retains changesInReviewBehavior=ERROR_IF_IN_REVIEW and stops on ongoing-review
errors; it never retries with a review-cancelling mode. Only internal is mutated.
Normal Google automatic review handling applies to this owner-authorized internal
release; delivery timing remains controlled by Google.
Grant no production permission to this service account.

The service JSON stays on bastion; OAuth tokens are transient in memory; temporary
RSA assertion-signing files are inside0700folders and cleaned. HTTPS redirect
forwarding of Google authorization is disabled; resumable sessions accept only
approved Google hosts. Private key/P12/password never leave bastion. OpenSSL,
Python3stdlib and fullJDK/keytool/jarsigner are required; no pip dependencies.
An existing service key cannot be silently replaced. Future approved app builds
require updated pins/program, while account/signing setup remains reusable.

## Evidence and limits

Google Android Publisher v3 discovery retrieved directly (with TLS verification)
SHA2569d2b7db45d63a0bd62c18d607d558392f8b63276bfb227ee1f2a5926f1ed5419.
Resumable path uses documented/resumable/upload/androidpublisher/v3/.../bundles.
Official commit/review semantics:
https://developers.google.com/android-publisher/api-ref/rest/v3/edits/commit

24local test scenarios cover internal-only transaction ordering, validation failure,
cleanup/idempotency/downgrade/hash guards, lost commit/chunk acknowledgments,
trusted upload hosts, redirect/credential redaction, private install/no-overwrite,
real disposable RSA JWT and full-JDK fixture signatures/payload tamper detection.
Host and fullJDKcontainer together cover all24 (each environment skips the single
fixture unavailable there). No test authenticates to Google. Owner installed the Google credential on bastion; live --check returned internal1030002.
The first --publish verified/signed/uploaded1030003andvalidated the edit, then got
the specific400above. No commit success is claimed until owner reruns1.1.

## Required step in every release handoff: activate update policy

The owner requires this step with EVERY new release. Upload/commit to Play alone
does not update the game's version policy. Each handoff must supply the exact
new numeric code in the server command, including when no backend deployment is
otherwise needed. Do not mark the rollout complete until the public policy is
verified. Keep this activation separate from the upload: wait until the new build
is available in Play to every intended player before raising the shared minimum.
An internal-only build must not become mandatory for production players.

For the current1030020, after that availability check, run as root on bastion:

```bash
python3 /opt/scorer/server/version_updates.py \
  --minimum 1030020 \
  --latest 1030020 \
  --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Verify both minimum_version_code and latest_version_code equal1030020. On the
next release, replace BOTH values with its actual code. Then open the older app
online and confirm that the mandatory update screen appears.
