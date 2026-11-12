# Verification — 12 November 2026

Source476f5759397adf5fd8b962956002cc3e70fc938c. Player screen shows actual values
without slash targets/progress bars; season and career remain separate and the
tracked career goals occur once. Monthly salary explicitly named without /month.
Nine catalogues format correctly with goals6/trust91/transfers0/caps0. Underlying
milestone award mechanics, saves and totals unchanged. Actual staged-production
reported-value screenshot inspected.24native player/layout/stadium/celebration
tests pass, including no-scroll screen bounds on1280x591and640x360.

Crowd10%above1030007(.90→.99;5→5.5px;38.75→42.625px), with feet/aspect, atlas,
seating and animations preserved. Total scale137.5%ofpre1030007. No player/keeper
or physical solver change; original PNGs unchanged.

AAB117223459bytes, SHA256
59f90f7fa12fe762fddf4bb76152e726db0d9a44f956e7e2ca18e737db793bf8.
Numeric1030008/name1.0/World/production. bundletool/118ELF/16KiBZIP checks pass.
Matching Python independently inspected packaged version, stats-screen headings,
absence of target bars from that screen and enlarged crowd constants.

Successful delivery actions:
https://github.com/pereiragoncalo/Scorer/actions/runs/43225146916
https://github.com/pereiragoncalo/Scorer/actions/runs/43225152351
Publisher fixture tests pass24cases, with actual AAB payload locally and JDK
fixtures in CI. Anonymous full AAB/coordinator/signing-helper/publisher downloads
match local bytes/SHA256. Transfer ref removed after verification.

Owner signing, internal Play commit, server minimum/latest activation and actual
phone acceptance require owner execution. Both commands in STATS_CROWD_1030008.md
and publisher1.6prints the activation reminder, AFTER Play availability to every
intended player. No live minimum, backend data or public-record setting changed.
Existing unrelated local WIP is preserved.
