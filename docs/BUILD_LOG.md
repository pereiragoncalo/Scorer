# Build log

## Packaging snapshot, 23/10/2026
- Google Drive v006 used as baseline.
- Verified local `python3 -m py_compile` succeeds.
- Android SDK/NDK and APK/AAB compilation: **not executed or verified**.
- Hardware smoke tests: **not executed**.

## Next run
Codex should append the exact commands, logs, test results and blockers for each task.

## 2026-10-23 — phase 1, source candidate 0.6.1

Read AGENTS.md, README.md, ROADMAP.md and FIRST_CODEX_TASK.md before edits.
Validated archive paths and baseline/main SHA256 against SOURCE_CHECKSUM.txt.
Imported starter in commit 957f7c5; retained Scorer history and a recoverable
Git bundle outside the checkout at /workspace/scorer-before-striker.bundle.

Changes: moved original simulation/career definitions into a headless career.py;
main.py keeps the original Kivy UI and imports its required core symbols. Added
private Android saves, legacy migration, atomic writes with visible error,
generic default Alex Silva, 13 regression/security tests, pinned host dependencies,
workspace Buildozer cache helper and candidate API 36/arm64/NDK28c settings.
No baseline changes; existing saved names remain unchanged.

Commands/results:
- `python3 -m py_compile main.py career.py tools/build_android.py`: PASS.
- `python3 -m unittest discover -s tests -v`: 13 tests PASS, none skipped.
  Covers imports without Kivy, career training/match progress, restart, v1/v2
  saves, invalid JSON, unknown migration versions, no-overwrite migration,
  write failure preserving previous save, private Android path via simulated App,
  FREE boundary, provider failure and save tampering unable to unlock WORLD.
- Installed Buildozer 1.5.0, Kivy 2.3.1, Cython 0.29.37 in external venv.
- `buildozer -v android debug`: FAILED on missing distutils with Python 3.12.
  Installed setuptools 75.8.2, retried: FAILED on read-only ~/.buildozer.
- `python tools/build_android.py -v android debug`: cache corrected; FAILED
  prerequisite check: Java compiler (javac) not found. Retried after spec update,
  same confirmed prerequisite. No native compilation or APK/AAB generated.
- `apt-cache policy ...`: system metadata has no candidates for checked build
  packages; system locations are read-only. Full build image still required.
- Kivy desktop smoke: initial KIVY_HOME parent missing, created parent and retried.
  App opened with SDL2/Mesa llvmpipe, ran event loop and stopped via Clock after
  two seconds, exit 0 and UI_STARTUP_OK. Not an Android/touchscreen test.
- `pyflakes main.py career.py tests tools`: initial unused imports cleaned.
  Remaining diagnostic is original UI local variable `score` assigned but unused;
  no undefined-name diagnostics. Full lint is therefore not a clean pass.
- Read-only upstream p4a clone at pinned commit: NDK recommendation 28c, AGP
  8.11.0, Python recipe 3.14.2, Kivy 2.3.1. Compatibility and 16 KB compliance
  remain UNVERIFIED until native build/output/device tests.

Security audit: no payments enabled; FREE remains fail closed. Baseline excluded
from APK sources to avoid shipping its personal default name. Original optional
Wikipedia badge fetch/image URLs and generated sound/cache paths require follow-up
review. Static reference manifest does not prove actual package policy. No secret
or signing key created. This is not a complete security certification.

Next task: provide full Android build prerequisites, generate debug APK, verify
manifest/ELF alignment and install on real Android hardware before ad-board work.

## 2026-10-23 — resolve cloud toolchain blockers (0.6.1 tooling revision)

No game logic, baseline, payments or advertisements changed in this revision.
The managed Docker daemon was healthy (28.4.0, vfs). Prepared a Docker toolchain
instead of requiring writes to the read-only host system. Added tools/android/
Dockerfile, setup.sh, install_sdk.sh and run.sh; tools/build_android.py now omits
environment values on failures. Added a security regression test for that behaviour.

Evidence and corrections:
- Pulled Python 3.12 Bookworm image with verified Docker digest; pinned digest
  14a4933e6cef421424f7a66d89a3f4eafcbd0d90e0a822251f298e05132dc735.
- Docker build initially needed writable buildx state: BUILDX_CONFIG moved under
  /workspace/striker-android-build/buildx, preserving registry configuration.
- Built image with JDK 17.0.20.1, autoconf 2.71, cmake 3.25.1, compilers and tools.
  Verified executable presence and `pip check` (no broken requirements).
- Mounted session/system CA bundles; refreshed Java trust store outside image.
  Git initially failed TLS trust; added GIT_SSL_CAINFO/CURL_CA_BUNDLE and reran
  with verification enabled. Python user installation initially tried /.local;
  set PYTHONUSERBASE to writable cache and added its scripts directory to PATH.
- Retrieved official SDK metadata using TLS and verified package archives against
  published checksums. Owner accepted Android SDK licence explicitly in chat.
  Latest command line tools changed --licenses semantics; used pinned CLI 19.0.
  Installed API 36, build-tools 36.0.0, platform-tools 37.0.1 and NDK r28c.
  sdkmanager install exited 0. A repeat run of `bash tools/android/setup.sh`
  completed with exit 0, including all 14 tests passing and SDK already installed.
- Buildozer's initial automatic update also installed build-tools 37.0.0. Disabled
  future broad automatic updates via APP_ANDROID_SKIP_UPDATE. No claim that
  native/Gradle build tool selection has been verified.
- Native preparation advanced to SDL2_image/libjxl recursive submodules. Build
  FAILED: proxy CONNECT 403 for https://skia.googlesource.com/skcms. No APK/AAB.
  Partial libjxl submodules need `git submodule update --init --recursive` after
  policy activation; do not silently skip this just because directory exists.
- Current tests: `python3 -m unittest discover -s tests -v`: 14 PASS, no skips.
  Shell syntax checks and Python compilation of build wrapper PASS.
- Saved additive custom network domains (preserving presets): drive.google.com,
  drive.usercontent.google.com, www.openssl.org, openssl.org,
  download.savannah.gnu.org, maven.google.com, skia.googlesource.com.
  These are DRAFT settings, not proven enforced. User review/save/publication
  is required before the blocked operation can be retried meaningfully.
- Drive download still returned 403 before policy activation. No Drive connector,
  runtime identity or secrets are configured. A network allowlist cannot provide
  private-account access; no OAuth credentials were requested or invented.

No hardware USB devices or /dev/kvm are exposed by this machine. Android hardware
acceptance, final manifest checks, ELF 16 KB alignment, signed release generation
and Drive upload remain pending. See ANDROID_BUILD.md for exact resume commands.

Additional tool verification:
- NDK clang 19.0.1 executes; sdkmanager --list_installed confirms the package
  versions above. `adb devices -l` initially failed because numeric Docker user
  had no writable account home. Added an unprivileged passwd account in the
  image with home /work/cache/user (without setting HOME). Retest exited 0;
  daemon started and device list is empty.
- A setup rerun overlapped an in-progress edit of install_sdk.sh and exited 2
  while reading the changing script. Validated the stable script with bash -n
  and reran the installer successfully. Final full setup rerun is recorded in
  /workspace/striker-android-build/cache/setup-final.log.
- The SDK setup now checks the SHA256 of the licence text accepted in this chat;
  changed licence terms stop setup for owner review rather than being accepted
  silently. This is a licence-change guard, not an artifact checksum override.

## 2026-10-23 — after user publication: real debug APK build

Runtime status now reports configuration revision 2 and the published custom
hosts. Actual Git read to skia.googlesource.com/skcms succeeded (exit 0); the
network policy state itself is reported unknown, so readiness is based on that
specific successful operation. Completed libjxl's pinned recursive submodules.
No second publication was required for the previous network blocker.

Native build completed host Python 3.14.2, libffi, OpenSSL, Python arm64, SDL,
pyjnius and Kivy. Source build fallback warnings about missing prebuilt wheels
were expected and did not establish failure. Actual later failures and fixes:
- Isolated pip lost certificate environment variables. Added a supported pip
  cert configuration at cache/user/.config/pip/pip.conf, preserving other options.
  Test without PIP_CERT/SSL_CERT_FILE/REQUESTS_CA_BUNDLE successfully fetched the
  setuptools index. No trusted-host flag or TLS bypass used.
- Gradle Java did not consume HTTP_PROXY/HTTPS_PROXY. Added Java proxy properties.
  First derived them outside Docker, where hostname proxy is outer-only; that
  failed UnknownHostException. Corrected derivation inside Docker using its
  reachable inherited proxy. Gradle then downloaded and built successfully.
- Added four configuration/security tests: pip settings preserved/repeatable,
  invalid pip config preserved, Java uses managed proxy, and proxy credentials
  are rejected without disclosure. Total: 18 PASS on Python 3.12 and built
  host Python 3.14.2; no skips.

First generated APK failed static native checks: chardet 7.7.0 bundled 17 Linux
x86_64 extensions (e_machine 62), also with insufficient 16 KB alignment. Rejected
that artifact. Pinned chardet==5.2.0 (pure Python) in buildozer.spec. A naive
rebuild retained the stale distribution because p4a matches recipe names, not
versions. Removed only the generated dist and stale chardet target files while
retaining native build caches. Packaging venv then exposed two pip versions
(25.3/26.2.2 metadata) and failed BuildDependencyInstallError import; recreated
only that generated venv. Rebuild exited 0, producing corrected debug APK.

Final artifact:
- bin/striker-0.6.1-arm64-v8a-debug.apk (20,761,765 bytes)
- SHA256 00211bb14422a9eeff5b4ab6ba3ea227b2e174c490fee7dbfdca215b61586a2b
- `apksigner verify --verbose`: PASS, v2, one debug signer.
- `zipalign -c -P 16 4`: PASS.
- tools/android/verify_elf_alignment.py: PASS, all 118 ELF files AArch64 and
  LOAD alignment >= 16 KB, including extensions inside compressed libpybundle.so.
- chardet 5.2.0 import and ASCII detection in built host Python: PASS.
- aapt: package com.clemir.striker, version 0.6.1, min SDK 26, target/compile 36,
  native arm64-v8a, landscape, no requested permissions.
- Generated debug manifest has debuggable=true and allowBackup=true. The reference
  release policy is not merged; backup/release policy remains a release gate.
- Earlier repeat packaging warnings about SDL Java patches were checked using
  reverse patch dry runs: both succeeded, proving patches already applied.
- App private payload has 4 entries (career/main/sitecustomize bytecode and p4a
  environment settings); no baseline/tests/tools packaged.

Game logic/baseline unchanged in this revision. No Android device installation,
touch gameplay, lifecycle persistence or 16 KB device execution was performed.
No AAB, release signing, public publication, payments or sponsor work performed.
Next: install corrected debug APK on real Android hardware and execute the
functional acceptance checklist before considering release or ad-board work.

## 2026-10-23 — 0.6.2 responsive menus and exit

Owner reports 0.6.1 runs on an Android phone without crashes; menu text overflow
was observed. This is owner feedback, not a full automated hardware acceptance.
Owner clarified product: FREE has exactly one division, funded exclusively by
stadium advertising; World is a separate paid app with fictional defaults and a
local name editor/importer. Updated AGENTS/ROADMAP and docs/PRODUCT_MODEL.md.
No payments, paid artifact, advertisements or remote name downloads added here.

Changes:
- Added menu_ui.py: native Kivy layouts for offers/hub/training/standings/scorers/
  calendar/agent/world, wrapped labels, adaptive columns, vertical/horizontal
  scrolling, 52 dp touch buttons and fixed navigation header. Compact hub puts
  Play/actions before statistics. Menu tree is retained between frames and only
  rebuilt when career/view state changes. Stadium, simulation and career logic
  remain the original Python/Kivy implementation.
- main.py routes real widget touches before game shooting, adds save/exit modal,
  prevents simulation advancing while exit confirmation is open, and saves on
  Android pause/stop. A failed explicit save prevents exit. Menus can fit portrait
  windows; gameplay retains landscape. No claim about all possible device/notch
  configurations without device tests.
- career.py reports save success/failure and fixes the pre-existing current_club
  reference in the local rename method. Tests prove edited names/progress survive
  restart. New FREE career division displays fictional Divisão Striker; existing
  saved/custom names remain compatible. FREE menu/action guard hides paid editor
  and World actions; save edits still cannot unlock World.
- buildozer.spec 0.6.2, excludes ui_tests from APK. Development requirements add
  pinned pytest for Kivy's real touch-test helpers. Baseline unchanged.

Validation:
- `python3 -m unittest discover -s tests -v`: 20 PASS, no skips.
- `KIVY_HOME=/workspace/striker-runtime/kivy /workspace/striker-venv/bin/python
  -m unittest discover -s ui_tests -v`: 8 PASS, no skips. Includes 7 menu views
  across 640x360, 800x360, 960x540, 1280x720, 360x800 and 320x240 (42 layout
  combinations), system font scale 1.6, native touch navigation, training/game
  transition, visible Play button, cancel exit, save-before-stop ordering and
  remaining open after save failure. Numeric cells stay within their rows.
- Initial GUI test dependency pytest was missing; installed/pinned it, then reran
  real tests successfully. A first Widget.export_to_png capture did not represent
  live rendering, so inspected actual App event-loop Window screenshots instead.
  Corrected table minimum width to account for cell spacing/card padding so
  trailing numeric columns are reachable by horizontal scrolling.
- Live Linux SDL2/Mesa app opened and produced reviewed screenshots at 960x540,
  640x360 and 360x800. These are desktop renders, not Android store screenshots.
  UI result logs/screenshots: /workspace/striker-runtime/menu-tests/.
- Python syntax, pyflakes on menu_ui/ui_tests/changed career tests and diff
  whitespace: PASS. No claim that all legacy main.py lint warnings were fixed.
- `bash tools/android/run.sh python tools/build_android.py -v android debug`:
  PASS, actual native APK, final log cache/build-0.6.2-final.log.
- Actual final APK: signature v2 PASS, `zipalign -c -P 16 4` PASS; all 118 bundled
  ELF libraries AArch64 with LOAD alignment >=16 KB PASS. Development signing
  certificate matches 0.6.1; package/application ID retained for in-place updates.
- APK private payload includes career/main/menu_ui/sitecustomize bytecode and p4a
  environment file, with no tests/baseline/tools.

Artifact: bin/striker-0.6.2-arm64-v8a-debug.apk (20,774,313 bytes)
SHA256: 87b55632503d132a357fec2c3583d29715d2d3b23d02b9c51623b9859327b387
Copy: /workspace/deliverables/Striker-0.6.2-arm64-debug.apk

Limitations: new APK not yet tested on the owner's phone. No release APK/AAB,
public distribution, real advertisements or paid World application. Existing
World simulation has full-depth European pyramids but only one tier in many
other countries; a true worldwide all-divisions product and safe name importer
remain future tasks. Next: owner tests update-in-place, scrolling/text, exit and
career recovery; then offline fictional stadium advertising.

## 0.6.3 — SCORER, splash e auditoria de UI/persistência

Pedido do proprietário: Sair exclusivamente no menu principal, corrigir texto
sobreposto do resultado, splash com jogador a rematar/crédito clemir e auditoria.
Nome corrigido pelo proprietário para SCORER, texto do splash em inglês.

Ficheiros: `main.py`, `menu_ui.py`, `career.py`, `buildozer.spec`,
`assets/splash.png`, testes de carreira e Kivy, README e relatório
`docs/AUDIT_0.6.3.md`. Motor e baseline preservados.

Validação: py_compile dos três módulos, 21 testes de carreira/build/segurança e
10 testes Kivy aprovados. Captura da janela Kivy 1280×589 inspecionada após
corrigir a configuração inicial do tamanho da janela do capturador (primeira
captura tinha viewport de 800 px). Não confundir com teste Android.
Compilação real: `bash tools/android/run.sh python tools/build_android.py -v android debug`.
Assinatura v2 debug, ZIP 16 KB e todos os 118 ELF AArch64 alinhados a 16 KB.
Mesmo certificado e applicationId da beta 0.6.2. Sem permissões solicitadas.
Logs completos no ambiente: `/workspace/striker-runtime/build-0.6.3-final.log`,
`verify-0.6.3.log`; próxima tarefa é validar esta atualização no telemóvel,
percorrendo splash, menu, treino, oportunidade, resultado e gravação/reabertura.
Sem validação física de 0.6.3, sem AAB ou assinatura release nesta etapa.
