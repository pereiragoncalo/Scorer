# Scorer World 0.6.36 — coherent wordmark lettering

Owner screenshot showed the mismatch between the raster SCORER wordmark and the
separate Barlow Condensed WORLD label. Removed that label. World now renders one
transparent SCORER WORLD PNG edited from the existing project artwork, with the
same extended italic letter design, gold bevels and aligned word baseline. This
is artwork matching, not a claim to have recovered an unknown original font file.
Free continues to render the unedited original assets/menu_logo.png.

The image-generation tool produced assets/menu_logo_world.png (2197x716 RGBA).
Its PNG bytes are preserved unchanged; Kivy displays a TextureRegion
(16,186,2180,350), omitting transparent canvas margins. No PIL/runtime resampling
or new font dependency is introduced. One Image supplies the complete World
wordmark across entry, normal hub and compact hub. Top-left alignment, aspect
ratio, compact confirmation, banner guards, language/career behaviour remain.
Free staging removes this World-only artwork.

Changed: menu_ui.py, assets/menu_logo_world.png, tools/prepare_editions.py,
buildozer.spec0.6.36/code1026636, existing staging and brand UI tests, docs.
193 tests PASS (122 core/security+71 actual Kivy). Existing brand assertions now
check a single correct asset/region instead of a separate WORLD text widget;
staging verifies World retains the exact PNG and Free omits it. All prior
modal/backup/banner/locale/save/gameplay tests pass. No gameplay or SDK changes.

The actual World arm64 debug APK compiled and passed package/version/launcher,
same debug signature, bundled edition/UI bytecode/PNG SHA256, no-ads/no-Billing,
font/language content, ZIP16KB and118 ELF alignment checks. Full APK/image hashes
in WORLD_WORDMARK_0.6.36_artifact.json. PNG SHA256:
8faf2466b210e6d84ece82321f158c45b6c12084b08e4e3e47d46686ab0b1989.
Generated from the owner's existing menu logo using the image-generation tool;
no external font or third-party logo was fetched.

[Inspected desktop Kivy entry](captures/world-wordmark-0636.png), not an Android
screenshot. Logs: /workspace/striker-runtime/wordmark-core.log, wordmark-ui.log,
build-0636-world.log. No new Free APK needed;0.6.35 remains its latest artifact.
Unrelated unfinished World WIP was preserved. No actual phone test, production
signing, payment/ad activation or Play upload claimed. Next: install World over
0.6.35 and confirm the unified lettering on entry and both main-menu layouts.
