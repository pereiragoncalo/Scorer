# Scorer0.6.45 — automatic aggregate usage

Owner observed second opening finally arrived, confirming delayed delivery/view
rather than proof of permanent transport failure. Owner now explicitly requires
no user toggle. No speculative Android transport replacement was made.

Production app factory uses mandatory mode for Free Android, World Android and
Windows. It is enabled immediately, old Off preference cannot disable it, and
set_enabled(False) is rejected in mandatory mode. Removed both UI toggle actions
and controls. Generic optional counter class remains for backwards-compatible
unit/synthetic-probe testing; actual app factory always selects mandatory mode.

Splash clearly states usage counts are sent automatically; Privacy explains
fields/destination/retention and shows Automatic, with no On/Off option. Play
privacy/data inventory updated accordingly. No covert collection, device/name/
career/contact/session identifiers or raw session histories added. Same9numeric
allowlist, first-party daily aggregates, HTTPS endpoint,7day local expiry and90day
server totals. Cloudflare processes connection/IP information as disclosed. Games
remain playable offline; delivery queues/retries use0.6.44 code. No ads return.

Public name/team season records remain separately optional with explicit share
confirmation and removal. No automatic publication or secret-token changes.
No server upgrade, credentials, DNS or historical-total editing required.

IMPORTANT publication review: making analytics mandatory is NOT proof it is
legally/Play compliant. Automatic collection must have an appropriate legal basis
and meet Google User Data/Families rules, including the mixed-minor audience.
Aggregate-only payload does not exempt transport/IP or device-access requirements.
Public policy/contact, accurate mandatory collection declarations, adult controls/
moderation for public chosen names, release signing/testing remain outstanding
before production. Owner requested this QA behavior; no store approval claimed.

Tests: compulsory factory, no disable UI/action, stored old Off overridden, restart
and two-opening counting, optional public name sharing independent. Ordinary UI
fixtures explicitly use optional/local mode to avoid sending test events; real
Windows frozen smoke asserts actual factory mandatory+enabled, overrides sender
before App.on_start so NO artificial QA counters reach owner. Existing separate
opening probe remains synthetic/no-network. Artifacts checked after builds.

Verification:180core/security+99Kivy tests PASS (279 unique). Native Windows run41248241931/source52db76ad passed6staging checks and frozen smoke, including automatic factory, visible splash notice and two foreground openings. Both actual APK factories tested from packaged bytecode: automatic enabled, disable rejected, controls absent; synthetic transport disabled. Both APK signatures match the existing debug key, ZIP16KB/118ELF16KB verified; DEX contains no ads/UMP/billing SDK. Windows unsigned; Android debug QA; actual phone testing remains pending.

[Scorer-Free-0.6.45.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.45/Scorer-Free-0.6.45.apk)
[Scorer-World-0.6.45.apk](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.45/Scorer-World-0.6.45.apk)
[Scorer-Free.exe](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.6.45/Scorer-Free.exe)
