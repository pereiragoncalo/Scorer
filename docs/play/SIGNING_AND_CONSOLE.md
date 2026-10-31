# Protected signing and final Console steps

The owner confirms the developer account is active/verified. No Console token or
upload keystore is configured in the cloud. Do not paste private keys/passwords
into chat or commit them. No new production key was generated in the cloud.

1. In each app's Console signing page establish whether it is NEW enrollment or an
   existing signing identity. Existing apps must follow their registered upload
   key/reset procedure; do not generate a replacement by assumption.
2. For genuinely new enrollment, run tools/play/create_upload_key.py on the owner's
   laptop with a fresh protected keystore path. It prompts twice without echo,
   uses keytool env password handling, file0600 and refuses overwrite. Back up
   key+password securely in separate safe storage. The public upload certificate
   can be shared/enrolled; the private key cannot.
3. Use Play App Signing. Distinguish upload key from app signing key that signs
   installed Play packages. Different signing identities from current debug APKs
   prevent ordinary in-place replacement: export/verify career recovery first.
4. Complete actual review flags/configuration described in RELEASE_0.6.46.md;
   select an unused increasing versionCode for EACH package and stage production
   via tools/prepare_editions.py --channel production. Build AAB release.
5. Inject SCORER_UPLOAD_KEYSTORE, SCORER_UPLOAD_ALIAS, SCORER_UPLOAD_STORE_PASSWORD
   and SCORER_UPLOAD_KEY_PASSWORD securely on the owner's machine and use
   tools/play/sign_aab.sh INPUT.aab OUTPUT_SIGNED.aab. Password values must never
   appear in argv/logs. The script reads them via JDK env selectors.
6. Inspect signed bundle + generated APK with tools/play/verify_bundle.sh. Pass
   free|world explicitly and SCORER_UPLOAD_CERT_SHA256 from Console. Production
   rejects the known DEBUG certificate and wrong expected cert. Rehearsal bundles
   are not final signed releases. Native library/metadata checks do not establish
   legal clearance or real-device operation.
7. Create/update TWO listings, free pricing, approved names/contact/policy and
   artwork plus real Android screenshots. Complete IARC/target audience/minors,
   Data Safety, no ads/no in-app purchases and app access. No game login; private
   statistics administrator token is NEVER a reviewer credential.
8. Internal test from Play, pre-launch/16KB/real phones and signature-transition
   recovery tests. Run closed-test/production-access steps only if shown for the
   apps; prior verified account status does not prove or disprove that requirement.
9. Confirm final artifact, checksums, source, policy, operator/moderation readiness,
   countries and release notes; obtain owner approval for the concrete upload and
   rollout. No Console submission or publication is performed by these scripts.
