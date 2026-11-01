# Scorer World 0.9 QA acceptance candidate

[Download World0.9 APK](https://github.com/pereiragoncalo/Scorer/raw/refs/heads/beta-0.9/Scorer-World-0.9.apk)

Point1 implementation completed: persistent continental/national competitions and qualifiers, domestic brackets, played promotion playoffs, balanced club movement, next-season entry fields and saved history. Inspect them under World > Competitions. Formats are explicit game rules, not verified official competition regulations.

Export a career backup, then Save and Exit, install over the matching World QA app and Load Game. Existing career IDs and imported aliases are retained. No extra server update is needed for these offline competition features.

348tests passed. Seeded three-season engine check:148controlled personal fixtures,9reloads, no repeated fixture or backward date. Actual APK bytecode, package/certificate and118ELF/16KB verified. These host checks do not replace real Android acceptance. APK retains the DEBUG upgrade key; public1.0 production signing/Play approval remains separate.

[Formats and evidence](WORLD_COMPETITIONS.md) · [Verification](verification.json) · [Remaining launch steps](https://github.com/pereiragoncalo/Scorer/blob/main/docs/play/ROAD_TO_1.0.md)

International fixture lists and calendar rows resolve imported club names by stable identity; national names use the selected UI language.
