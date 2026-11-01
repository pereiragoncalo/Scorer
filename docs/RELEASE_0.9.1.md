# Scorer World 0.9.1 QA

VersionCode 1026901; public launch remains 1.0. World only, free, no adverts/IAP, included names editor.

## Startup notice

The splash leads to a scrollable notice with exactly two fixed buttons, OK and NOT OK. OK continues and permits automatic aggregate delivery; NOT OK quits immediately, clears pending unsent counts and prevents the stop callback from adding/transmitting counts. Each new process shows the notice, including existing installs. Back during the notice quits in the same way. No career is deleted. The in-app privacy-request workflow is removed, including the packaged client module, callbacks and translations. Server legacy records are retained for compatibility; no database/tunnel/token changes and no live policy deployment were performed.

## Editor

World main/compact hub → Names Editor → Import Names File at the top. Android uses the existing system document picker, then preview and confirmation. Packs are local display aliases; careers/UIDs are retained. The complete Europe/Brazil/Argentina pack remains in docs/data/name-packs.

## Physical saves

The old keeper moved its body onto the predicted ball lane while extending both hands beyond it. High central/near shots passed above the body, while low shots met the body or perfect ground-level gloves. The new keeper leaves lateral room for its visible arms, aims gloves at the committed predicted lane within a bounded reach, jumps earlier/higher for high balls and takes longer to get down for low balls. Vertical judgement has a small fixed error per shot. Training uses the same height-aware movement, based on the current division rather than stale match opponents. Ball launch/aim/gravity, goal dimensions, shared render/collision skeleton, field collisions and career opportunities remain unchanged. No goal cap or recent-score rubber band.

The paired seeded test uses 120 targets/powers per height band in each context (1,800 actual fixed-step shots before and after). Goal outcomes include the real keeper, field collisions and goal frame. The prior corner-only benchmark missed the high/low imbalance. These are controlled simulation rates, not human goals per match or real phone tests.

| Division/context | Low before → after | High before → after |
| --- | --- | --- |
| 4 / training | 3.3% → 11.7% | 94.2% → 16.7% |
| 4 / easy | 6.7% → 24.2% | 91.7% → 45.8% |
| 4 / hard | 0.0% → 2.5% | 60.0% → 8.3% |
| 1 / easy | 2.5% → 10.0% | 81.7% → 22.5% |
| 1 / hard | 0.0% → 2.5% | 40.8% → 5.8% |

[Raw evidence](data/shot_heights_0.9.1.json), reproducible with `tools/calibrate_heights.py`. The World competition/save migration implementation from 0.9 is retained. Host Kivy tests and compiled APK checks do not establish real Android acceptance or Play approval. APK retains the existing debug QA upgrade certificate; export a backup before changing to a future Play-signed install.

## Validation

232 core tests passed. Native Kivy suite: 112 passed initially, two new fixture/assertion failures corrected, then both new tests passed (114 unique UI tests, 346 total). Paired physical calibration: 1,800 actual simulated shots per build. Actual APK verified: package/version/code, existing upgrade certificate, zip alignment, 118 native ELF libraries with 16KB support, exact compiled source, startup transmission gate/rejection, absence of the removed client module, editor SAF bridge and competition/save-reload smoke. No Android handset or Play Console test was performed.
