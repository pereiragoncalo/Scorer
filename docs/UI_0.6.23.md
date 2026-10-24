# SCORER 0.6.23 — first post-match ad and optional morale reward

## Owner report and changes

Owner confirms the 0.6.22 entry banner displayed on the phone, but no post-match
ad was seen. The previous three-match/180-second gate can explain that observation;
it does not prove the SDK's interstitial failed. No device logs were available.

- Remove initial three-match wait. First completed match can show a ready TEST
  interstitial on final CONTINUE. Subsequent full-screen breaks require 60 seconds;
  never show at half-time/in a chance, wait for ads, or show a late load in play.
  Prefetch at match start as well as career entry and final whistle. Unavailable
  inventory, consent or SDK failures still skip the ad. Availability/error codes
  are exposed in Privacy rather than pretending an ad was presented.
- Training has WATCH AD: +1 MORALE, a voluntary standard RewardedAd (not rewarded
  interstitial). Google onUserEarnedReward alone creates the local reward receipt;
  load, presentation and dismissal never grant morale. User can continue ordinary
  training/play without this ad. Reward capped at 20 morale, once per career week.
- Reward ads prefetch when opening training. If not ready/offline, explain and
  allow training; repeated taps do not award points. Training availability/session
  limits, energy rewards and mandatory weekly practice remain independent.
- Native receipt is UUID + opaque career/week hash, stored in app-private
  SharedPreferences; never passed to AdRequest. Python consumes it once, atomically
  saves +1 morale and weekly receipt fields, then acknowledges native receipt.
  Save failure rolls back all reward fields and keeps receipt for retry. Replay
  after save/before acknowledgement is idempotent. Old-week/different-career receipts
  cannot grant current rewards. Legacy saves default to no reward claimed; save v2
  and package are preserved. A new season resets the weekly availability.
- Poll local reward receipts/status once per second while a career is selected,
  including after returning from the ad; no network polling loop is added. Pending
  native receipt can be recovered after process recreation and career reload.
- An accepted optional rewarded ad also starts the 60-second full-screen cooldown,
  preventing a forced interstitial immediately after a voluntary video. Ad requests
  remain child/under-age tagged, non-personalised, G-rated and UMP-gated. Official
  TEST rewarded unit: ca-app-pub-3940256099942544/5224354917. Still no revenue.
- Compact training actions side-by-side; combined energy/morale row, smaller
  explanatory text. Test caught 8px overflow in the initial layout; tightened card
  spacing/removed duplicated energy text, reran full Kivy tests successfully.

## Tests and actual build

59 core/build/security tests + 42 real Kivy tests pass (101 total). Coverage:
first-match eligibility, 60-second cooldown, no late/duplicate breaks, optional
reward cannot create points merely by request, callback receipt consumption,
weekly limit, 20 cap, context mismatch, save failure/retry, replay after reload,
button disabled after claim, persistent morale and all existing schedule/training/
menu/touch/gameplay regressions. Syntax, git whitespace and baseline hash pass.

Real desktop GL capture at 1280x589/density1.64 inspected:
/workspace/striker-runtime/scorer-0623-training0001.png. It shows the training
menu/space, not an Android ad. Actual 0.6.23 ad presentation/reward still needs
phone validation. Mock receipts do not prove a video completed on a real device.

Actual Android APK compiled including RewardedAd, native callback/receipt code,
all three official TEST units and advertising.pyc. Package com.clemir.striker,
version1026623, target36/min26, same debug signaturev2. ZIP16KB and all 118 AArch64
ELF alignments pass; AD_ID and three AdServices permissions remain absent; no
private signing keys or career saves in payload. No new permission added.

APK 37,181,442 bytes, SHA256
5477d0272298ae493294f22cf40bf83c64eaffc338e9618043840b5715754dcd.
Logs build-0.6.23-final.log and verify-0.6.23.log in striker-runtime outside Git.
Files: advertising.py, Java ScorerAds, career.py, main.py, menu_ui.py,
buildozer.spec, controller/core/Kivy tests and docs/AGENTS/README.

Next: phone test first final CONTINUE (without having just watched a reward ad),
optional reward completion/early close/failure, +1 morale saved/reloaded, weekly
limit and offline fallback. If unavailable, inspect Privacy's separate break/
reward status. Production still needs owner account and FOUR public IDs: app,
banner, interstitial, rewarded (reward amount1/typeMorale), approval and review.
