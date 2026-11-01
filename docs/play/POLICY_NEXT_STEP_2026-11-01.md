# Public documents — next step after the laptop's HTTP503

Owner supplied: Gonçalo Pereira, goncalo@clemir.com, both apps free, audience
includes minors. The screenshot confirms the operator installed the server,
health returns true, public records schema3 works and maintenance timer is active.
The policy installation refused the incomplete example configuration.

## Work delivered

server/public.policy.review.json fills the date and all five previously incomplete
policy areas with facts, source references and an explicit proposed basis. It is
marked publication_status=draft. No review flag is set true and no unverified
legal basis or account configuration is represented as approved.

/privacy is a full PT/EN review proposal with a prominent DRAFT banner and noindex.
The date is the proposal update date, not a fabricated final effective date.
/terms contains the actual in-app community rules in Portuguese and English.
/delete contains real in-app removal and public email support instructions.
Terms/removal require valid identity/contact, but no longer unnecessarily depend
on finalizing the analytics basis. The final-policy validation remains strict.
Older complete configurations remain readable, with a draft warning when no explicit status exists. The installer preserves rather than replaces a complete legacy policy.

The draft states what the apps/collector actually do. It describes Cloudflare
using current public documentation, without claiming zero provider logs, EU-only
processing, accepted contracts or account settings not inspected here. The basis
of legitimate interests is explicitly a PROPOSAL, with outstanding necessity,
proportionality, objection and minors' requirements. Continue is not treated as
consent. A self-declared adult DOB/PIN is not called verified parental consent.

## Review and installation

Preview HTML files in policy-preview/ are generated from the actual renderer and
configuration. They contain no JavaScript, trackers, admin token or personal game
records. See [privacy preview](policy-preview/privacy.html),
[terms](policy-preview/terms.html) and [removal](policy-preview/delete.html).
Do not just send the new JSON to the old configure_public command: the new
renderer is what makes the draft status visible.

The narrow installer server/install_public_policy.py copies only:

- /opt/scorer/server/public_pages.py
- /opt/scorer/server/configure_public.py
- /opt/scorer/public.json (the explicit proposal)

It stops/restarts scorer-online briefly to avoid an old cached renderer displaying
new configuration without the warning. It verifies all three loopback pages and
the draft marker; on failure it restores the prior files/configuration and starts
the previous service again. It refuses symlink targets and refuses to replace an
existing completed policy with a draft. It does not read/edit SQLite, administrator
credentials, cloudflared, the maintenance timer or careers. Service startup can
still perform its normal pre-existing retention housekeeping.

Local validation requires no root or service changes:

```sh
python3 server/install_public_policy.py --check
```

The deployment command uses a fresh pinned worktree on the laptop; the final
reply supplies the concrete revision. If a complete policy has already been
installed independently, preserve it instead of using this draft installer.
No cloud SSH access is available, so public installation is not claimed here.

## Evidence and scope

13 focused tests pass: complete/missing/malformed/oversized configuration;
PT/EN and visible draft status; HTML escaping/no JavaScript; exact match with
existing app rules; unchanged false production review flags; real local HTTP200
for all public documents and private totals remaining404; no usage events from
page views; narrow update with untouched secret/database sentinels; rollback for
failed verification/missing old config; refusal to downgrade completed/legacy policies
and refusal to follow symlinks. CLI --check passes.

Official pages fetched HTTP200 on2026-11-01, extracted text hashes retained in
[evidence](evidence/2026-11-01-policy-sources.json):

- https://www.cloudflare.com/privacypolicy/
- https://www.cloudflare.com/cloudflare-customer-dpa/ (version6.4 effective2026-04-03 on fetched page)
- https://www.cloudflare.com/trust-hub/gdpr/
- https://support.google.com/googleplay/android-developer/answer/10144311?hl=en
- https://support.google.com/googleplay/android-developer/answer/9893335?hl=en

Cloudflare's DPA/DPF/SCC descriptions are not evidence of account-specific adoption
or configuration. Google expressly requires applicable legal requirements and
disclosures even where another lawful basis is used. Public HTTP200 for a draft
is not a final Play privacy policy or approval to ship mandatory analytics to
minors. Production review requirements remain unchanged. The current APKs/EXE/AABs
are not rebuilt because no client code changed.
