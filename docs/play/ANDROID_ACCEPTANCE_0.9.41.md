# Android acceptance — Scorer World0.9.41

The owner reports the three requested0.9.41 phone smoke checks **passed**:
startup/policy, team talk/training/tap/unlock, and completed match/save/exit/reload.
See docs/data/android_acceptance_0.9.41/owner-smoke.json. Model and Android version
were not supplied. Extended checks and Play installation remain pending; existing
automated/static evidence is not a substitute for them. Use the current DEBUG QA APK, signed by the same existing QA key:
https://github.com/pereiragoncalo/Scorer/releases/download/qa-0.9.41/Scorer-World-0.9.41.apk

Keep the existing installation/data. Export a private career recovery file before
uninstalling or later moving to the differently signed Play installation. Do not
send saves, PINs, private ownership credentials or screenshots containing them.

Record device/Android version and Pass/Fail for these checks:

1. Start: app info says0.9.41, splash advances on one deliberate touch, compact
   launch notice is readable and both agreement/exit actions work. Agreement
   alone does not enable statistics or record sharing.
2. Policy: Help → Settings → Full Privacy Policy opens the final English GitHub
   Pages privacy URL. Its navigation opens community/removal documents. No draft
   banner; developer Gonçalo Pereira/contact goncalo@clemir.com.
3. Existing career: load without losing club/goals/trophies/purchases. On a new
   installation use a new local career. Avoid New Game over an existing save.
4. Team talk/training: choose offered focus, complete the three practice attempts;
   one tap advances each result once, last result opens summary, Play unlocks at
   the appropriate point. Touch does not accidentally launch the next shot.
5. Match: one full official fixture, aim/shot/result/score visible, no crashes;
   newspaper then due team talk flows correctly; return/save.
6. Recovery: background/resume and close/reopen/Load retain the recorded career
   progress. No duplicate salary/rewards or replayed completed results.
7. Offline: with internet disabled, local load/training/match/save still work;
   an online-service error does not block the career.
8. Editor/SAF: export the current local names to a user-chosen Downloads file;
   preview/import the same file and cancel safely if desired. No broad-storage,
   location, contacts or advertising-ID prompt should appear.
9. Privacy controls: statistics initially off. Adult PIN required for separate
   opt-in; Stop Statistics & Erase Unsent needs no PIN and leaves career playable.
   Do not publish personal information during QA. Career online server currently
   returns404 until the bastion update; record that as a known service blocker.

For internal Play acceptance repeat these checks on the Play-installed signed
build, test debug-to-Play career export/import, capture genuine Android store
screenshots and inspect the pre-launch report. Do not replace these pending
results with desktop or source-test evidence.
