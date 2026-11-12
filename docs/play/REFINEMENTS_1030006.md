# World 1.0 / 1030006 — five refinements

- Update check: small white text at bottom left, visible only on the splash while
  checking. No normal-check modal or gameplay lock. A cached/new mandatory
  minimum still blocks and opens Update/Retry/Exit; offline policy unchanged.
- Estate: render only bought house/car/clothes. No studio fallback. Existing
  genuinely purchased assets remain; new players own none.
- Contract salary: monthly quote/display/payment at the first career date in a
  new calendar month. No fixture/reload duplicate payment. Version2 life state
  preserves balances and inventory. Legacy weekly contracts convert once by
  52/12 to retain annual value; no retrospective extra payouts are invented.
- Player: season objectives and all career milestones in two compact columns,
  including progress bars, name field, contract summary and reachable actions.
  No ScrollView on this screen.
- Match opportunities: clear-chance probability falls to6% for strong opponents,
  12% for medium opponents, at most22% for weaker ones. Penalty event chance falls
  from18% to5% per match. Weighted non-repeating ordinary plans favour crosses,
  deep crosses, corners, free kicks and22–29metre long shots. Match score expectation
  uses the same5% penalty probability. No forced misses or physical solver changes.

All supported languages have monthly salary/long-shot labels and updated help.
Startup agreement still activates statistics. Save/package/signing identity and
existing catalogue colours/names remain unchanged. Server deployment is not needed.
The operator minimum is not automatically raised to an internal-only version.

## Existing bastion installation (root)

```bash
(
set -eu
scorer_release=$(mktemp -d /root/scorer-release.XXXXXX)
curl -fL --retry 2 https://github.com/pereiragoncalo/Scorer/releases/download/play-automation-v1.4/bastion_play_internal.py -o "$scorer_release/uploader.py"
printf '%s  %s\n' 299d8c82bf649a2aad8480b5f3c282f65164deb51f29a5cb01d796e73e79f3a9 "$scorer_release/uploader.py" | sha256sum -c -
install -m700 "$scorer_release/uploader.py" /root/scorer-signing/play-internal.py
python3 /root/scorer-signing/play-internal.py --publish
)
```

Uses existing installed Google service account and owner upload key. Downloads,
checks and signs the approved1030006 locally, then publishes INTERNAL only.
After Play makes it available to every intended player, activate the update
policy on bastion before calling this rollout complete:

```bash
python3 /opt/scorer/server/version_updates.py \
  --minimum 1030006 \
  --latest 1030006 \
  --name 1.0
curl -f https://stats.clemir.com/v1/app-version
```

Confirm both codes in the public response are1030006, then reopen the old app
online, use Update and verify the five changes on the phone. An internal-only
version must not become mandatory for production players.

## Verification

22focused life/migration/opportunity tests and53career/presentation tests pass.
18native update/player/estate/opportunity UI tests pass; a further targeted
three-test run passed after the language-font adjustment. Real native phone
layouts at1280x591and640x360 confirm all profile controls fit without a scroll.
Actual staged production Portuguese player/estate/splash screenshots inspected.
Normal check stays white and nonblocking; a known minimum still opens the gate.
Delivery/static APK evidence will be recorded after final audit. Actual owner
signing, Play acceptance and physical-device smoke are not inferred from CI.
