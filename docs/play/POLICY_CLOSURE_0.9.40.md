# Policy remediation — Scorer World0.9.40

Owner confirms the game uses fictional clubs. The separate local editor is retained;
this release does not bundle the owner's optional real-name import pack or claim
club licensing/affiliation. Original generated game artwork and bundled font/data
license notices are retained. No official badges are fetched by the shipped path.

## Implemented

- Statistics are optional and off by default. Old mandatory-enabled state is not
  voluntary permission: the new versioned opt-in rejects that legacy state and
  never sends its counters. No forced choice between analytics and playing.
- A separate disclosure and adult PIN are required to enable statistics from
  Help → Settings. Startup I AGREE only acknowledges the notice. Playing/training/
  saving and public record sharing remain independent of statistics.
- Stop Statistics & Erase Unsent requires no PIN. Stops future events/delivery,
  deletes pending counters and persists withdrawal; on save failure it fails
  closed for this process and attempts to remove the old choice file. A request
  already transmitted cannot be recalled. Anonymous combined totals cannot be
  split to remove a person's contribution.
- Social sharing remains default-off, adult-managed and separately explicit.
  A clear online/real-world safety reminder now precedes sharing and appears in
  adult controls. It is translated into all9UI languages. Reporting, blocking,
  terms, pending review and withdrawal of Season/Career records are retained.
- English public policy now describes voluntary statistics, both record categories,
  current local language behavior, fictional purchases and external email feedback.
  App support remains Gonçalo Pereira / goncalo@clemir.com. Privacy stays in Settings,
  accessible via Help; there is no new main-menu privacy button.
- Combined owner-run installer updates the policy and v3/v4 service with rollback
  on failed local verification. It preserves records, credentials, maintenance and
  Tunnel configuration; may add the additive career table. It does not set any
  review flag, create a Console app or submit a release.

## Bastion installation

Download the exact committed `docs/data/server/Scorer-Play-Policy-0.9.40.py` over
HTTPS, run `python3 FILE --check`, then run `python3 FILE` as root on bastion.
It targets /opt/scorer and scorer-online, with local port8787 by default.
Review the public URLs from a normal browser afterwards:

- https://stats.clemir.com/privacy
- https://stats.clemir.com/terms
- https://stats.clemir.com/delete

The privacy page should say Optional usage statistics, mention the Career category
and identify Gonçalo Pereira. Public HTTPS must work without login, geofencing or
an access challenge. Local200 does not establish external access.

## External conditions still not observable here

This cloud has no SSH connection to bastion. Public policy requests receive403
from this environment; the owner confirms the phone opens the OLD test/draft page. The owner must execute the installer/check external access;
we cannot truthfully say the new policy is live yet. The server's actual moderator
must operate the queue/respond to reports and privacy email; code does not replace
ongoing moderation. The adult PIN is an access safeguard, not verified identity or
parental relationship. Follow applicable parental-authorization law and truthful
Console audience/IARC/Data Safety answers. No legal opinion/Google approval is
created by passing tests or accepting the startup notice.

The candidate still needs release signing, Android/Play acceptance and Console
forms. Previous0.9.39 APK does not contain these changes. Do not use its automatic
analytics behavior as the description of this new candidate.
