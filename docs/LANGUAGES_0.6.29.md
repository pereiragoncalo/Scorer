# SCORER 0.6.29 — edition-specific languages

Owner request: English-only Free; nine languages in the separate World app.
No change to simulation, shot physics, competition formats or career identifiers.

## Behaviour

| Product | UI languages | Default / controls |
| --- | --- | --- |
| Free | English only | Fixed, no locale read, preference file or language selector |
| World | English, Portuguese (Portugal), Spanish, German, Italian, Korean, Japanese, Simplified Chinese, Vietnamese | Primary system language; unknown language falls back to English; Language on entry and Help; Automatic resets to the phone |

World's manual preference is an atomic private scorer_language.json version1
file, independent of striker_world_career.json. Invalid/oversized preferences
fall back safely. A write failure leaves the prior selection and career intact.
Changing system language on resume updates Automatic only and preserves editable
text/cursor/focus. Language selection does not change country suggestions, clubs,
contracts or the career. Portuguese regional variants share PT-PT; Chinese scripts
share Simplified Chinese in this version. No Internet or translation API is used.

209 source messages have matching translations/placeholders in all nine
catalogues: menus, training, notices, scoreboard/time, contracts, agent/status,
editor/validation, privacy, help and save/exit dialogs. 212 country/football-region
labels have separate localized presentation. Canonical keys/callbacks never
change. Custom club/player/league names (including names such as PLAY or HELP)
remain literal. The editor's version1 JSON schema, IDs and editable values remain
unchanged. Generic Division/National Cup labels translate; custom titles remain
opaque. Branding stays SCORER/by clemir and the existing splash artwork is retained.

World uses bundled Barlow Regular for Latin/Vietnamese and the regional Japanese,
Korean and Simplified-Chinese Noto Sans CJK regular OTFs. No runtime font download.
The 49.3MB uncompressed CJK fonts increase World's APK size; Free stages neither
the fonts nor any translation/country catalogues. The three regional fonts cover
all used UI/country characters and the tested accented/custom Asian names.
Font caching includes the selected font. Compact tables and paginated language
controls retain the correct locale during asynchronous Kivy layout callbacks.

## Changed areas and provenance

- localization.py: offline catalogues, language/preferences, opaque names, dates,
  country/league display and script/font selection.
- ui_localization.py, main.py, menu_ui.py, world_ui.py: translated UI/canvas,
  language screen, input/JSON preservation, async/paged table presentation.
- device_locale.py: nine language codes, independent existing country detection.
- assets/i18n: nine message catalogues, countries.json, Babel/Unicode licences.
- assets/fonts: full Noto regional fonts and OFL licence. Exact official pinned
  source URLs, sizes and SHA256: [font_sources.json](i18n/font_sources.json).
- Country labels derive from Babel2.17.0/Unicode CLDR, with explicit football-region
  names. Reproduce with tools/build_ui_countries.py (Babel development dependency).
  FontTools is development-only for glyph coverage. Neither package ships as an
  Android Python dependency. Translations were authored for this release; native
  speaker proofreading remains useful, especially for long labels on real phones.
- tools/prepare_editions.py, tools/play/prepare.py, buildozer.spec: explicit JSON
  whitelist, .otf packaging, edition stripping, version0.6.29/code1026629.
- tests/test_localization.py and ui_tests/test_world_languages.py add focused
  regression/security/layout tests. No career schema changes.

## Validation

118 core/security and61 actual Kivy interface tests PASS (179 total), including:
Free ignoring locale/preferences, nine phone-language mappings, fallback,
manual persistence/atomic failure/malformed preferences, complete placeholders,
all translated glyphs, opaque custom names/career bytes, input/JSON preservation,
Android resume, asynchronous table headings and native canvas/clock textures.
Language controls pass 1280x640,640x360,360x640 geometry/touch checks at density1.6.
Japanese Help, Korean hub and Chinese language-picker desktop Kivy screenshots
were rendered and visually inspected; they are not Android screenshots.
[Japanese Help](captures/ja-help-0629.png), [Korean hub](captures/ko-hub-0629.png),
[Chinese language picker](captures/zh-language-0629.png).

Core/UI logs: /workspace/striker-runtime/i18n/core-final.log and ui-final.log.
Real sequential Android QA build logs: /workspace/striker-runtime/build-0629-free.log
and build-0629-world.log. Exact artifact verification and sizes are recorded in
[LANGUAGES_0.6.29_artifacts.json](LANGUAGES_0.6.29_artifacts.json).

Rebuild using fresh output directories:

```bash
python tools/prepare_editions.py --edition free --output /workspace/Scorer-free-0629
python tools/prepare_editions.py --edition world --output /workspace/Scorer-world-0629
SCORER_SOURCE_ROOT=/workspace/Scorer-free-0629 bash tools/android/run.sh python tools/build_android.py -v android debug
SCORER_SOURCE_ROOT=/workspace/Scorer-world-0629 bash tools/android/run.sh python tools/build_android.py -v android debug
```

Both actual final APKs passed package/versionCode1026629/targetAPI36 checks,
valid same-certificate signatures, ZIP16KB alignment and all118 AArch64 ELF LOAD
alignments >=16KB. Actual bundled edition.pyc was evaluated with Python3.14:
Free WORLD_BUILD=false, World=true, WORLD_PREVIEW=false in both. Actual World
payload contains all nine209-message catalogues,212-country data and exactly the
three source-hash-matched regional Noto fonts; Free contains none of those assets.
Neither contains BillingClient; World contains neither AdMob nor Internet
permission, while Free retains only the existing test ad setup.

These are arm64 debug QA APKs signed with the existing certificate; separate
packages update their corresponding0.6.28 app without uninstalling. No physical
Android language test, AAB/store upload, release signing, payment activation or
production ad activation is claimed. Existing unfinished World tournament work
in the main checkout was preserved separately from this tested release snapshot.

## Next Android checks

1. Install both APKs over0.6.28; confirm their independent careers still load.
2. Set phone to Portuguese: Free stays English, World Automatic shows Portuguese.
3. Change all nine World languages; check buttons/help/training/match/standings,
   rotation, keyboard, goal notices and at least one complete save/reload cycle.
4. Type an accented/Asian player or club alias; switch app/phone language while
   editing and confirm text/career/JSON stay unchanged. Test editor SAF import/export.
5. Verify World stays offline/ad-free; Free test ads and stadium promotion remain
   unchanged. Real phone performance/font memory and native-speaking proofreading
   remain required before a public store release.

Integration check: the main checkout with its preserved unrelated World WIP also
passed the same118 core/security and61 Kivy tests after the three-way merge.
