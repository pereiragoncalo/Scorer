# Scorer World 0.6.47 — launch preparation

Launch product: Scorer World, com.clemir.scorerworld, free, no adverts, no IAP, local names editor included. No Free listing is planned. Public documents and store copy are English; game UI retains nine languages. Existing independent QA installs and saves are retained.

## What changed

Production staging rejects Free. English World privacy/terms/removal documents identify Gonçalo Pereira and goncalo@clemir.com. The final policy reflects the owner's report of Cloudflare Tunnel/proxy only and legal exceptions to automatic usage. A real in-app Privacy rights procedure immediately suspends collection and clears queued counts; the new private server queue lets the operator grant requests. Only the requester can withdraw; server confirmation and the next opening are required for resumption. No case identifier is included in ordinary usage or aggregate backups.

## Laptop deployment

The previously installed English/Portuguese draft is not this final policy. A full server update is required before the final policy because the privacy-request endpoint is new. Use a fresh pinned checkout as root; the earlier publicacao checkout is root-owned. Exact safe.directory applies only to that path and command, not globally. Do not paste/read administrator credentials.

The final delivery provides pinned commands. Run `bash server/install_online.sh`, then `python3 server/install_public_policy.py` from that reviewed checkout. The first preserves the existing administrator credential, database and tunnel and installs additive rights-case storage. The second transactionally installs only public documents/configuration and rolls back on failed local checks. Existing records remain subject to moderation. Verify /health and /privacy, /terms, /delete externally, including `data-publication-status="published"` and English-only World content. In /admin, the operator can load pending privacy requests using the existing token. Never request a client's secret token; use its public reference.

## Remaining steps before Google Play

1. Install/verify the new laptop server and final policy; check an actual current World request offline/online and operator grant/withdrawal. Source/local tests are not a laptop deployment.
2. Confirm human moderation and support coverage, actual applicable legal/children/provider arrangements and truthful Data Safety/target-audience forms. The final policy is not Google approval or verification of parental identity.
3. Use the protected upload key and Play App Signing, production staging with explicit completed review fields, unused increasing versionCode and a verified signed AAB. The delivered debug APK and unsigned rehearsal AAB are not upload-ready production releases.
4. Install through Play internal testing; test real Android/16KB devices, editor/import/export and save recovery across the debug-to-Play signature transition. Capture genuine Android screenshots. Complete any closed-test/production-access requirements shown by this account.
5. Complete ONE free World listing, IARC, app access (no login), no ads, no IAP and countries, then approve the concrete signed artifact/rollout. Never use the private statistics admin token as a reviewer credential.

See SIGNING_AND_CONSOLE.md, DATA_SAFETY.md and STORE_LISTING.md. No Console submission or rollout was performed by this preparation.
