# Automatic aggregate usage — concrete assessment for operator review

Owner: Gonçalo Pereira; privacy/support: goncalo@clemir.com. Both apps are free,
ad-free and include children in their intended audience. The owner requires
usage counts to be automatic, without an in-game disable switch.

## Actual safeguards implemented in 0.6.46

Nine bounded counters only, no player/device/session identifiers in usage payload;
no exact event timestamps or raw diagnostic text. Local queue expires after seven
days; server keeps combined receipt-day totals90days and periodic cleanup also
runs without new traffic. HTTPS certificates verified. No raw request/IP/UA logs
in collector. No advertising/billing SDKs. Usage transmission waits for the
first-run detailed notice to be acknowledged; public names require independent
adult-managed access, accepted terms and explicit Share. These are separate flows.
No PIN or birth date is uploaded. DOB is checked then discarded locally. Adult
PIN uses salted PBKDF2 and persisted lockout; it is not verified identity or proof
of legal parental consent.

## Proposed basis and unresolved decision

A possible basis for aggregate product analytics is legitimate interests in
understanding operation and improving a free game. The payload minimization and
absence of profiles/advertising reduce risk. However, convenience to the owner
does not prove necessity or override children's rights. Counts are not needed to
play offline. The owner must assess necessity/alternatives, users' reasonable
expectations, proportionality, the applicable national rules on device storage,
minors, and how objections would be honored when the owner requests no switch.
The processor's handling of IP addresses remains relevant even if our own totals
cannot be attributed to a person.

The Continue button is acknowledgement of a notice, NOT freely given analytics
consent. Do not label it consent or silently set legal review flags. If the
applicable assessment requires opt-in/withdrawal or a different arrangement for
children, implement that before production; this engineering work does not grant
an exemption. An app-store declaration cannot replace a lawful basis.

## Operator evidence still needed

- Reviewed basis/necessity/balancing record, with particular assessment of children
  and practical handling of rights/objections.
- Actual Cloudflare configuration, processor terms, geography, retention/logging
  and applicable transfer safeguards. No access to those account settings here.
- Operator adoption of the terms/moderation process and prompt response to
  goncalo@clemir.com. The code does not provide human moderation by itself.
- Effective policy date and approval of the final text after deployment settings
  are confirmed. Complete server/public.example.json and publication review config
  only with true facts. Empty legal/provider fields intentionally prevent a draft
  policy from being served as a completed production policy.

See the official User Data and Families sources linked in the audit. Production
staging blocks while these operator attestations are missing; rehearsal AABs
remain available for technical verification. This is not a legal opinion.
