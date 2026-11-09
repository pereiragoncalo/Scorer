# Scorer World 1.0 candidate — Google Play policy audit

Decision: **compliance is not yet established; do not describe this candidate as fully compliant.**
This is an implementation/evidence audit, not Google approval or a legal opinion.
Reviewed the 0.9.39 candidate source a3bc694 and matching current safety/UI/server
files. No game changes, declarations, Console submission or live server writes.
Official policy pages below were retrieved successfully today; source hashes/status
are in evidence/2026-11-09-policy-sources.json.

## Findings

| Area | Evidence | Disposition before public release |
| --- | --- | --- |
| Public privacy policy | In-app Help → Settings → FULL PRIVACY POLICY exists (contextual_help.py, menu_ui.py). Developer identity, contact, retention and Cloudflare are described in policy source. Today's public URL fetch returned HTTP403, previously error1010. | **Unverified public access.** Check ordinary browser and reviewer access; fix Cloudflare restrictions if they prevent public access. A cloud403 alone does not prove all visitors are blocked. Google requires an active publicly accessible, non-geofenced HTML policy. |
| Policy accuracy | docs/play/PRIVACY_POLICY.md and server/public_pages.py cover optional completed-season records but do not clearly describe the newer Career category. Policy legal-basis text says Continue acknowledges and is not consent, whereas launch notice says I AGREE. Local careers section says phone language while current default is English. | **Documentation changes required.** Reconcile current Season/Career data, English default and acknowledgment/consent wording across app, published policy and Console. The Data Safety inventory already flags current additions; that is not a deployed policy. |
| Automatic usage and minors | anonymous_stats.py sends nine counters after launch acceptance, with no ordinary disable switch; no device ID in usage payload. Cloudflare receives connection/IP information. Local7day/server90day expiry. | **Unresolved assessment.** The switch absence alone is not a universal Play violation. Determine applicable child-data/legal basis and any consent/objection requirements; do not present an agree-or-exit button as sufficient legal consent by itself. Declare required app interactions and assess diagnostic counts/provider processing accurately. |
| Children/social features | Local adult birth-date check, PIN, sharing off by default, terms and explicit Share exist. Terms say use nicknames, no school/contact details. | **Partial implementation.** These are permitted types of adult-action mechanisms under Families, not proof of verified parental authorization. Strengthen the explicit online-safety/real-world-risk reminder before sharing; current text mainly prohibits personal information. Declare actual audience and information-sharing features in IARC/Console; do not choose adult-only to avoid requirements. |
| Public leaderboard UGC | online_leaderboard.py, server/moderation.py and career_records.py implement report/block/withdrawal, pre-moderation, terms, hashed owner credentials and pending/approved states. | **Code present, live operation unverified.** Exercise both Season/Career end-to-end, withdrawal while locked, reports and operator response. User previously requested an owner-run bastion installer; no evidence here that current v4 deployment/operator coverage is complete. Mere endpoint/code existence is not ongoing effective moderation. |
| Deletion | In-app stop-sharing/removal and public /delete source; no email/password login. Persistent publisher identity still exists. | Verify live deletion route and support handling. Assess whether publisher creation constitutes account creation for Play's deletion rule; absence of an email/password login does not by itself settle that definition. |
| Advertising/payments/permissions | World staging strips billing/ad source; no monetization SDK; only INTERNET/ACCESS_NETWORK_STATE. Lifestyle money/purchases are fictional and local. | No observed ad/billing policy issue in candidate evidence. Declare no ads, no real in-app purchases. Recheck actual final AAB manifest/dependencies; base buildozer.spec is not staged release identity. |
| Intellectual property | Original sprite generation/font/data licenses exist; club references, kits/facts and separate real-name imports remain. No evidence of complete third-party rights clearance. | Review included assets, data licenses/attribution, real names and store images. An editor, factual name, club colours or a non-affiliation disclaimer does not alone establish infringement or clearance. Do not claim all assets licensed or official club affiliation. |
| Technical/distribution | Existing0.9.39 evidence: API36/min26/arm64,118nativeELF16KB checks, automated core/native/responsive checks. QA APK uses DEBUG certificate. | Signed production AAB, real Android testing, Play pre-launch results, truthful listing/screenshots and Console forms still required. Not a finding that current gameplay violates policy. |

## Verification performed for this audit

- Re-read official full User Data, Families, UGC and Intellectual Property policies.
- Compared network payload, local adult controls, policy-link navigation, public
  policy source, both leaderboard implementations and World staging configuration.
- Ran `python3 -m unittest discover -s tests -p 'test_publication_safety.py' -v`:
  **13 passed**. Covers local safeguards/notice gating, server moderation/removal,
  transfer/retention behavior. It does not test live Cloudflare, real phones,
  operator availability or legal compliance.
- No broad gameplay regression rerun: no runtime files changed.

## Concrete closure sequence

1. Update policy wording for Career records/current behavior and strengthen safety
   reminder, preserving small startup notice and no privacy button on main menu.
2. Confirm public policy HTML accessible without login/challenge and deploy matching
   policy; verify v4 moderation/report/withdrawal with owner-managed service.
3. Resolve required analytics/child-data treatment and rights obligations with actual
   deployment evidence; do not fake publication review flags.
4. Complete rights inventory and actual Console audience/IARC/Data Safety forms.
5. Build signed AAB, test through Play and on Android, then review final release.

The owner may create a draft app in Console; that is distinct from this report
certifying the declaration or authorizing a public rollout.

## Official sources

- [User Data](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en)
- [Families](https://support.google.com/googleplay/android-developer/answer/9893335?hl=en)
- [User Generated Content](https://support.google.com/googleplay/android-developer/answer/9876937?hl=en)
- [Intellectual Property](https://support.google.com/googleplay/android-developer/answer/9888072?hl=en)

## Subsequent implementation

Owner clarified that clubs are fictional. The former rights uncertainty is not
a finding of infringement. See POLICY_CLOSURE_0.9.40.md for the optional-statistics,
policy and family-safety changes; this original audit records the earlier0.9.39.
