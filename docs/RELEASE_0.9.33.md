# Scorer World 0.9.33 QA

The ball and supporters now use original retro pixel sprites. The animated ball remains a visual layer over the existing independent ball physics. Home and visiting crowds retain club palettes, separate celebrations and static fluorescent-green steward lines.

Attendance follows each team's collective points per game and league position, with a gradual early-season transition. National teams use recent collective results. Each home/away sector fills from its highest rows down, including upper tiers, with a scattered partially filled boundary row. Attendance is frozen for the fixture; goals do not instantly refill the stadium. This is a game presentation model, not official ticket-sales data.

Winning an observed collective league, domestic cup, continental cup or national title queues an eleven-player celebration: the squad approaches its own supporters and the captain raises a gold trophy. A dedicated coach talk follows. A due weekly club talk merges its two mandatory training-focus choices into this special talk. Personal scoring awards, qualification and promotion playoffs do not trigger collective championship celebrations. The queue and presentation stage survive saves; old trophies do not replay when loading an older career.

The existing gameplay, hitboxes, ball solver, club colours and approved player/goalkeeper art remain unchanged. New scene assets comprise 108 supporter cells, eight ball frames and one trophy. Textures use nearest-neighbour filtering, bounded palette caching and context-reload data; supporters remain two batched meshes rather than individual widgets.

This is a debug-signed World QA candidate, not a Google Play production release. Physical Android testing remains pending.

Validation: 407 core cases passed (three existing skips), plus eight focused scene/title cases including a played World cup final; 231 responsive presentation cases passed with zero findings. Additional title-talk layout checks cover all nine languages with and without a due weekly focus choice. The actual APK passed package/version, existing certificate, all118 ELF16KB alignment, ZIP alignment, exact sprite/source payload and packed career/title persistence checks.

Headless measurement (not a handset performance claim): 1,953 visible supporters, two team meshes, about1.85ms per crowd-motion update across300 updates, zero new texture allocations during animation; three scene palette textures retain279,936CPU bytes. Both versions of the special coach talk passed54 measured layout cases across all nine languages.

Final native validation: all211 Kivy UI tests passed. The four new scene/title tests also passed against the clean staged World source used for the actual APK.
