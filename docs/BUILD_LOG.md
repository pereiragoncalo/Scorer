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

## 0.6.4 — menu sem scroll, caixas compactas e ícone

Feedback do proprietário: caixas demasiado grandes, menu principal com scroll,
crédito clemir insuficiente; pedido adicional de ícone profissional.

Alterados `menu_ui.py`, `ui_tests/test_menus.py`, `assets/splash.png`, novo
`assets/icon.png`, `buildozer.spec`, README, AGENTS e `docs/UI_0.6.4.md`.
Main menu passa a dashboard sem ScrollView, com seis ações simultaneamente
visíveis. Painel final dimensionado ao conteúdo, botão de largura limitada.
Splash e ícone originais gerados para esta aplicação; splash inclui a assinatura
«SCORER by clemir» com destaque. Simulação, baseline e saves não alterados.

Verificação: py_compile; 21 testes sem interface e 11 testes Kivy aprovados.
Novo teste cobre seis combinações de ecrã/densidade, limites dos botões,
alvos de pelo menos 48 dp, ausência de sobreposição e ausência de ScrollView.
Capturas reais da janela Kivy 1280×589/densidade 1,64 inspecionadas: identificada
e corrigida concatenação de linhas de estatísticas e ordem dos campos durante
mudança de dimensões. Última captura do menu: `scorer-064-hub0003.png` no
runtime; captura do painel: `scorer-064-match0001.png`. Não são capturas Android.

Build real: `bash tools/android/run.sh python tools/build_android.py -v android debug`.
Assinatura v2 debug válida, mesmo certificado das betas anteriores; ZIP e 118 ELF
AArch64 com alinhamento 16 KB verificados. API 36/mínimo 26, mesmo applicationId.
Hashes dos recursos reais Android `res/mipmap/icon.png` e presplash e respetivos
assets privados conferem com as imagens fontes. Nenhuma chave de assinatura
incluída no APK. SHA-256 do APK:
`de061bd542b89488ede8f4161be609ed2e8a85caaec6409f2fe7d83d2bef1363`.
Logs locais `build-0.6.4.log` e `verify-0.6.4.log` em
`/workspace/striker-runtime`. Próximo: instalar atualização no telemóvel e validar
menu, ícone, splash e transições treino/oportunidade/resultado. Sem AAB ou build
release de loja nesta etapa; teste físico de 0.6.4 pendente.

## 0.6.5 — splash persistente, novo/carregar e FREE explícito

Feedback: splash desaparecia na rotação, faltava escolha de carreira ao abrir,
nome «England Division 4» sugeria várias divisões e menu precisava de redesign.

Alterados: main.py, career.py, menu_ui.py, assets/menu_stadium.png,
buildozer.spec, suites core/Kivy, README, AGENTS e docs/UI_0.6.5.md.
Detalhes e referência visual consultada (imagem de menu FIFA 2000) no relatório.
Não foi integrado código ou material de outros jogos. Novo fundo original.

25 testes sem interface + 15 Kivy aprovados (40). Comandos:
`python3 -m py_compile career.py main.py menu_ui.py`;
`python3 -m unittest discover -s tests -v`;
`KIVY_HOME=/workspace/striker-runtime/kivy /workspace/striker-venv/bin/python -m unittest discover -s ui_tests -v`.
Logs core/UI em `/tmp/scorer-065-core-final.log` e
`/tmp/scorer-065-ui-final.log`. Cobrem persistência do splash através de tempo,
rotação e toque real, carregamento explícito, ausência de autogravação antes da
escolha, confirmação/cancelamento/backup atómico, saves inválidos, transferência
FREE e duas épocas mantendo uma única liga, migração do nome sem perder progresso.

Capturas reais da janela Kivy 1280×589/densidade 1,64 inspecionadas: menu,
entrada e splash, em `/workspace/striker-runtime/scorer-065-*.png`.
Não equivalem a capturas nem testes Android. Baseline SHA-256 permanece
fed211d2ec63fe0275390b13ed4a1bcfcd18fa61238460b04b67d80ebca6205b.

Build real: `bash tools/android/run.sh python tools/build_android.py -v android debug`.
Logs `build-0.6.5.log` e `verify-0.6.5.log` no runtime. Assinatura v2 debug válida,
mesmo certificado, versão 0.6.5/API 36/mínimo 26/arm64. ZIP alinhado a 16 KB e
118 ELF AArch64 verificados. Ícone, presplash e assets (incluindo fundo novo)
conferem com fontes; sem saves, backups ou chaves de assinatura no pacote.
SHA-256 APK: 2334c6447665e711edf91d2f6cd70bd34b9acd360f824ec130adce21b2dca7e4.

Próximo: testar no telemóvel rotação/espera sem tocar no splash, toque para
Novo jogo/Carregar jogo e carregamento da carreira anterior, nome Liga Scorer e
navegação do menu. Sem teste físico desta versão, AAB ou assinatura release.

## 0.6.6 — nome do jogador, relevo e redução de scroll

Pedido: explicar/remover a imposição de Alex Silva, diminuir by clemir na mesma
posição, botões arredondados com efeito 3D e menos scroll nas páginas do jogo.

Alterados `career.py`, `main.py`, `menu_ui.py`, `assets/splash.png`,
`buildozer.spec`, testes, README, AGENTS e `docs/UI_0.6.6.md`.
Novo jogo exige nome antes do contrato; botão Jogador altera carreira existente
sem reiniciar. Renomeia também o marcador, valida nomes/colisões e reverte se a
gravação falhar. Botões partilham cantos arredondados, base, face elevada, brilho
e estado premido. Classificação, marcadores e calendário usam páginas sem
ScrollView, incluindo salto para clube/jogador e alternância de dados, sem
ocultar/remover registos. Cards compactados e propostas em duas colunas.

Verificação: py_compile dos três módulos; 27 testes core/build/segurança e 18 Kivy
aprovados (45). Primeira verificação detetou acesso errado a `.y` numa instrução
RoundedRectangle (API correta é `pos[1]`); corrigido no teste e no brilho do botão.
Suite final e capturas reais da janela Kivy inspecionadas: menu, classificação e
formulário, 1280×589/densidade 1,64. Não são capturas/testes Android.
Logs: `/tmp/scorer-066-core-final.log`, `/tmp/scorer-066-ui-final.log`.

Compilação real: `bash tools/android/run.sh python tools/build_android.py -v android debug`.
Logs runtime `build-0.6.6.log` e `verify-0.6.6.log`. Assinatura v2 válida e mesmo
certificado; versão 0.6.6/API 36/mínimo 26/arm64, ZIP 16 KB e 118 ELF AArch64
alinhados a 16 KB verificados. Ícone, presplash e novo código de perfil/listas
confirmados dentro do APK; sem saves, backups ou chaves privadas incluídos.
SHA-256: fae82e4dea96a491a66fef31cb31f081400a11016938a4208f6f3b7d884ba4b8.
Baseline mantém fed211d2ec63fe0275390b13ed4a1bcfcd18fa61238460b04b67d80ebca6205b.

Próximo: atualizar no telemóvel, alterar nome através de Jogador e verificar a
persistência ao reabrir, teclado, feedback dos botões e navegação por páginas.
Validação física desta versão pendente. Sem AAB ou assinatura release nesta etapa.

## 0.6.7 — alinhamentos e marca tipográfica

Pedido a partir de quatro capturas do proprietário: alinhar textos e melhorar a
fonte de SCORER by clemir. Marca nativa partilhada em Barlow Condensed ExtraBold
Italic + Barlow Regular, incluídas offline com licenças SIL OFL. Ajustados alinhamento
da entrada, identidade/indicadores e números/legendas da época; oportunidade e
resultado centrados. Face/rebordo dos botões alinhados com o centro do texto.
Seta não renderizada na energia do treino substituída por «para».

Ficheiros: menu_ui.py, ui_tests/test_menus.py, assets/fonts (2 TTF e 2 licenças),
buildozer.spec, README, AGENTS e docs/UI_0.6.7.md. Sem alteração do motor, carreira,
saves, arte do splash ou ícone. Fontes originais obtidas do repositório oficial
Google Fonts e redistribuídas sem modificações com a licença.

Verificação: py_compile; 27 testes core/build/segurança + 18 Kivy aprovados (45).
Suite Kivy final em `/tmp/scorer-067-ui-final.log`; core em
`/tmp/scorer-067-core.log`. Inspecionadas capturas reais da janela Kivy de entrada,
menu, treino concluído e oportunidade em 1280×589/densidade 1,64, runtime
`scorer-067-*.png`. Não são capturas Android.

Compilação real com `bash tools/android/run.sh python tools/build_android.py -v android debug`.
Logs `build-0.6.7.log` e `verify-0.6.7.log` em `/workspace/striker-runtime`.
Assinatura v2 válida, mesmo certificado, ZIP alinhado a 16 KB e 118 ELF AArch64
alinhados a 16 KB; Android API 36, mínimo 26. Confirmados hashes de ambas as fontes
e licenças dentro de assets/private.tar; novo BrandMark no bytecode e presplash
inalterado. Sem saves ou chaves privadas no pacote.
SHA-256: 0177f4bb804474b341b02a8b208aa2f8289acf5d30655bdb4e64ffead7297910.

Próximo: validar no telemóvel alinhamentos e renderização das fontes nos quatro
ecrãs enviados pelo proprietário. Versão beta debug, sem teste físico desta
versão, AAB ou publicação de loja.

## 0.6.8 — alinhamento, splash e treino semanal

Jogar alinhado às margens de Marcadores em landscape; ícone S seguido de CORER.
Splash gerado/revisto com pé esquerdo apoiado, direito recuado e bola no chão.
Uma sessão de treino por semana da carreira, reservada e gravada ao começar;
reabrir/abandonar não permite repetir. Bónus único, rollback em falhas de save,
compatibilidade com saves v2 anteriores, nova semana/época desbloqueia.

Ficheiros: career.py, main.py, menu_ui.py, assets/splash.png, buildozer.spec,
tests/test_career.py, ui_tests/test_menus.py, README, AGENTS, docs/UI_0.6.8.md.
Baseline preservado (SHA-256 fed211d2ec63fe0275390b13ed4a1bcfcd18fa61238460b04b67d80ebca6205b).

Verificação: 31 testes core/build/segurança + 22 Kivy passaram (53); py_compile
e git diff --check. Logs /tmp/scorer-068-core-final.log e
/tmp/scorer-068-ui-final.log. Corrigidos durante testes posição de Jogar em
retrato, dimensões antigas após mudança de densidade e resumo de treino cortado.
Capturas Kivy reais do menu e treino inspecionadas; não são capturas Android.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
Logs build-0.6.8.log e verify-0.6.8.log em /workspace/striker-runtime.
Assinatura v2 válida, mesmo certificado SHA-256
84c17cdf31e2ee7c6e9c082bde539df6822bf48267a0603de9814d6e2846ef49; ZIP alinhado
a 16 KB, 118 ELF AArch64 alinhados a 16 KB. API 36, mínimo 26, versão 1026608.
Confirmados splash/presplash, ícone, fontes/licenças e bytecode atualizado no APK.
Sem permissões declaradas, saves ou chaves privadas incluídas.
APK: 29 433 977 bytes. SHA-256:
44d3fe975b34e96f7095a426cb68f0d3b8fe69bd5d03bc18828941787557a4e2.

Próximo: atualizar no telemóvel e verificar alinhamento, splash e treino semanal
após reabrir/avançar semana. Beta debug, sem validação física desta versão,
AAB ou assinatura release para loja.

## 0.6.9 — base do nome alinhada com o ícone

Pedido: alinhar CORER com a parte inferior do S do ícone. O cabeçalho agora
agrupa ícone e palavra numa mesma linha, com altura partilhada e crédito
by clemir por baixo alinhado com o texto. Mantida a altura total do cabeçalho.
Ficheiros: menu_ui.py, buildozer.spec, README.md e este log.

31 testes core/build/segurança + 22 Kivy passaram (53), py_compile e
git diff --check. Captura real da janela Kivy em 1280×589/densidade 1,64
inspecionada em scorer-069-hub0001.png; bases visuais do S e CORER alinhadas.
Sem alterações à carreira ou aos seus saves. O primeiro comando de captura
falhou por xvfb-run não instalado; usado SDL_VIDEODRIVER=offscreen com sucesso.

APK beta debug 0.6.9 realmente compilado. Assinatura v2 válida, mesmo certificado
e identificador Android; ZIP e 118 ELF alinhados a 16 KB. Código atualizado
confirmado no pacote, sem saves/chaves privadas incluídos.
Logs build-0.6.9.log e verify-0.6.9.log em /workspace/striker-runtime;
testes /tmp/scorer-069-core.log e /tmp/scorer-069-ui.log.
SHA-256: 6fb5c0fe24463bbc1371a332201ccb195a68baef08625f61e88b4691e1eeaff0.
Próxima tarefa: confirmar alinhamento no telemóvel. Validação física desta
versão pendente; sem AAB/assinatura release nesta correção visual.

## 0.6.10 — jogo em inglês

Traduzidos menus nativos e Canvas, confirmação de saída/novo jogo, perfil,
erros de nome/save, contratos, agente, transferências, treino, jogo, datas,
tabelas, calendário e acesso World. Liga automática passa a Scorer League;
nomes personalizados não são traduzidos. Saves v2 anteriores mantêm progresso:
Liga Scorer migra, calendário histórico atualiza campos gerados e mensagem
transitória ao carregar passa a Career loaded. Esta edição permanece em inglês
independentemente da língua do Android; seleção automática não implementada.
Estratégia futura documentada em docs/UI_0.6.10.md.

Ficheiros: career.py, main.py, menu_ui.py, buildozer.spec, tests/test_career.py,
ui_tests/test_menus.py, AGENTS, README e docs/UI_0.6.10.md. Baseline preservado.

32 testes core/build/segurança + 23 Kivy passaram (55), py_compile e
git diff --check. Novo teste cobre meses em inglês e migração de feedback,
calendário e liga sem perda de nomes/progresso. Novo teste Kivy percorre sete
menus e valida feedback de nome. A primeira execução deste teste começou no
splash, pelo que o carregamento foi corretamente recusado e faltou MY POSITION;
corrigida a preparação para entrar em Start antes de carregar, sem relaxar
a asserção. Logs /tmp/scorer-0610-core.log e /tmp/scorer-0610-ui-final.log.
Capturas reais Kivy do menu e treino concluído inspecionadas em 1280×589,
densidade 1,64; textos visíveis. Não são capturas Android.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 versão 0.6.10, versionCode 1026610, API 36/mínimo 26.
Assinatura v2 verificada com o certificado anterior, ZIP e 118 ELF alinhados
a 16 KB. Strings inglesas conferidas no bytecode do APK. Sem permissões
declaradas, saves ou chaves privadas incluídos. Logs build-0.6.10.log e
verify-0.6.10.log em /workspace/striker-runtime.
Tamanho: 29434161 bytes. SHA-256: d1fd7b3614e2e26793bef67da4aa0d47b09ba8d5f7e24853f6f510865113f9e6.

Próximo: validar a versão inglesa no telemóvel, incluindo partida e diálogos.
Validação física desta versão pendente. Sem AAB/assinatura release nesta etapa.

## 0.6.11 — marcador fixo, flash de golo e intervalo

Marcador único no canto superior esquerdo, equipas em duas linhas, resultado
por linha e relógio à direita. Mesma geometria na simulação, aviso de oportunidade
e remate; barra inferior de tempo/data/competição removida. Avisos e contador
de remate posicionados abaixo do marcador. Flash verde local de um segundo
a cada golo simulado ou do jogador. Resultado do jogador atualiza no instante
do golo, com guarda por remate para não duplicar ao continuar.

Primeira parte termina aos 45 + descontos (1–4), com HALF-TIME e SECOND HALF.
Pausa mantém relógio parado; retoma aos 45:00. Mantidos descontos finais (1–8).
Timeline inclui ambos os descontos; apresentação desconta os da primeira parte
na segunda. Corrigido processamento de golos futuros antes de uma oportunidade
anterior: limitar avanço à oportunidade/limite da parte antes de processar eventos.

Ficheiros: main.py, menu_ui.py, buildozer.spec, ui_tests/test_menus.py, AGENTS,
README e docs/UI_0.6.11.md. career.py, saves e baseline preservados.

32 testes core/build/segurança + 27 Kivy passaram (59); py_compile e
git diff --check. Novos testes: pausa/retoma/descontos, oportunidade no limite
do intervalo, ordem de eventos, flash e contagem única do golo, desenho idêntico
em três resoluções/densidades e separação do contador de remate.
Uma execução expôs uma diferença de arredondamento de 0,000008 píxel na
asserção do contador, deixando densidade alterada para testes seguintes.
Aplicada tolerância de 0,0001 píxel e cleanup de densidade/janela no teste.
Suite final /tmp/scorer-0611-ui-final.log; core /tmp/scorer-0611-core.log.
Capturas Kivy reais de oportunidade, remate e intervalo inspecionadas em
1280×589/densidade 1,64, scorer-0611-*.png. Não são capturas Android.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.11, versionCode 1026611, API 36/mínimo 26.
Assinatura v2 válida com certificado anterior, ZIP e 118 ELF alinhados a 16 KB.
Código do marcador/intervalo confirmado no APK; sem saves ou chaves privadas
incluídos, sem permissões declaradas. Logs build-0.6.11.log/verify-0.6.11.log
em /workspace/striker-runtime. Tamanho 29434861 bytes.
SHA-256: d80a2eed88c29460672f35671f054ac9365236611e71aef4176c06ea5392c64b.

Próximo: testar no telefone golo a favor/contra, oportunidade e retoma após
intervalo. Validação física desta versão pendente; sem AAB/assinatura release.

## 0.6.12 — marcador compacto e treino obrigatório

Marcador reduzido de 360×64 para 280×46 dp; First half / Second half em vez
de 1H/2H. Mantido flash, relógio, intervalo e posição nas oportunidades.
Training movido para a esquerda de Play. Play cinzento/desativado até concluir
os três remates da semana; validação também em start_career_match. Data junto
a NEXT MATCH e quatro ações secundárias. Sessão de treino interrompida pode
ser retomada com contagem/golos persistidos após cada remate, sem novo bónus.
Campos opcionais v2 training_shots_taken / training_session_goals; reservado
legado sem contagem inicia com zero remates registados, sem bloquear a carreira.

A falha de oportunidade relatada não foi reproduzida no teste inicial. Mudado
o redesenho para manter MatchNotice na árvore de widgets, restaurando apenas
o Canvas, sem remover/repor o painel a cada frame. Teste de toque com cinco
frames entre pressionar/soltar cobre três oportunidades, incluindo descontos,
sem saltar nem consumir remate. Causa original ainda não confirmada no telefone.

Ficheiros: career.py, main.py, menu_ui.py, buildozer.spec, tests/test_career.py,
ui_tests/test_menus.py, AGENTS, README e docs/UI_0.6.12.md. Baseline preservado.
33 testes core/build/segurança + 29 Kivy passaram (62); py_compile e
git diff --check. Logs /tmp/scorer-0612-core.log e /tmp/scorer-0612-ui.log.
Testes novos verificam bloqueio/desbloqueio/rebloqueio semanal, contagem parcial
ao reabrir, rollback de gravação, bónus único, botões lado a lado e toques.
Capturas Kivy reais do menu e oportunidade inspecionadas em 1280×589/densidade
1,64. Não são capturas Android.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.12, versionCode 1026612, API 36/mínimo 26.
Assinatura v2 válida com mesmo certificado, ZIP e 118 ELF alinhados a 16 KB.
Código atualizado conferido no APK; sem permissões declaradas, saves ou chaves
privadas incluídos. Logs build-0.6.12.log e verify-0.6.12.log em
/workspace/striker-runtime. Tamanho 29436361 bytes.
SHA-256: 43988e5279b11f0812ad3843156d531f269c7fcb8dc530e57d6e5392996086fb.

Próximo: atualizar telefone, confirmar dimensões, completar treino e abrir
todas as oportunidades. Validação física e confirmação da falha reportada
pendentes. Sem AAB/assinatura release nesta etapa.

## 0.6.13 — dificuldade de finalização e logótipo

Pedido: reduzir facilidade excessiva, no máximo uma oportunidade fácil por
jogo e restantes difíceis; logótipo baseado no ícone, sem by clemir no menu.
Oportunidades pessoais limitadas a 0–3 consoante energia/moral. Uma oportunidade
fácil é atribuída em 60% das partidas, nunca mais de uma. Restantes remates
a 16,5–21 m e ângulo de 4,5–8 m, quatro defesas/barreira, menos tempo e GR
mais rápido. Penáltis/cabeceamentos/livres mantidos. Golos decididos pela física,
sem falhas impostas ou inflação de marcadores rivais. Totais antigos preservados.
Novo assets/menu_logo.png gerado com imagegen a partir do ícone original,
transparente, SCORER marfim/verde. Usado no hub e entrada sem crédito; ícone
e splash originais mantidos.

Ficheiros: main.py, career.py, menu_ui.py, assets/menu_logo.png, buildozer.spec,
tests/test_career.py, ui_tests/test_menus.py, tools/balance_shots.py, AGENTS,
README e docs/UI_0.6.13.md. Baseline preservado.
34 testes core/build/segurança + 31 Kivy passaram (65); py_compile e
git diff --check. Cobertura nova de 60 alocações sem dois lances fáceis,
posições/oposição/tempos, tipos de remate, reação do GR, treino e logótipo.
Uma asserção de visibilidade expôs inicialmente tamanho de widget não assentado;
fixado viewport explícito no teste. A execução seguinte confirmou recorte
real de ângulos extremos em landscape mais estreito. Reduzido o intervalo e
espelhado o mesmo ângulo para o lado visível quando necessário; suite final
aprovada em /tmp/scorer-0613-ui-final.log. Core /tmp/scorer-0613-core.log.

Ensaio físico reproduzível tools/balance_shots.py: 240 remates por perfil,
720 total, potência 0,85 e destinos amostrados com as mesmas seeds. Gerador
anterior: 109 golos/100 defesas/31 falhas (45,4%); fácil: 177/63/0 (73,8%);
difícil: 62/104/74 (25,8%). Todos resolvidos até 15 s simulados. Log
/tmp/scorer-0613-balance-release.log. Ensaio não mede habilidade humana,
classificação ao longo da época ou desempenho Android. O primeiro comando
do utilitário encontrou conflito dos argumentos com Kivy; corrigido com
KIVY_NO_ARGS antes da importação. Usa saves temporários isolados.
Capturas reais Kivy do menu, entrada e livre difícil inspecionadas em
1280×589/densidade 1,64; não são capturas Android.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.13, versionCode 1026613, API 36/mínimo 26.
Assinatura v2 válida com certificado anterior; ZIP e 118 ELF alinhados a 16 KB.
Logo e código de equilíbrio confirmados dentro do APK; ícone e splash
conferidos por bytes. Sem permissões declaradas, saves ou chaves privadas
incluídos. Logs build-0.6.13.log e verify-0.6.13.log em /workspace/striker-runtime.
Tamanho 30206997 bytes. SHA-256: ff747656022880c3d11cd0cf027c09babdf60f93f357eaa87b4824f9adb726c6.

Próximo: jogar várias partidas no telefone e avaliar conversão dos lances
difíceis. Validação física/equilíbrio humano pendentes. Sem AAB/assinatura release.

## 0.6.14 — contador agregado e iniciais do jogador

TIME TO SHOOT integrado numa faixa de 22 dp colada por baixo do marcador,
com a mesma margem esquerda e largura. Barra de progresso fina; duração,
dificuldade e cronómetro da partida não alterados.
Nome do jogador passa a ter inicial maiúscula em cada componente separado
por espaços ao guardar perfil ou carregar carreira. Mantidas grafia interna
e letras acentuadas. Migração da chave de marcadores acompanha o nome, sem
apagar golos. Colisão com outro marcador num save antigo mantém ambos os
registos intactos; editar perfil permite escolher nome sem ambiguidade.

Ficheiros: main.py, career.py, buildozer.spec, tests/test_career.py,
ui_tests/test_menus.py, AGENTS, README e docs/UI_0.6.14.md. Baseline preservado.
36 testes core/build/segurança + 31 Kivy passaram (67), py_compile e
git diff --check. Logs /tmp/scorer-0614-core.log e /tmp/scorer-0614-ui.log.
Cobertura de nomes acentuados, maiúsculas internas, migração com golos,
colisões, rollback e geometria do contador em três densidades.
Captura real Kivy scorer-0614-shot0001.png inspecionada em 1280×589/densidade
1,64. Contador agregado visível; não é captura Android.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.14, versionCode 1026614, API 36/mínimo 26.
Assinatura v2 válida com certificado anterior; ZIP e 118 ELF alinhados a 16 KB.
Código atualizado confirmado no APK; sem permissões declaradas, saves ou chaves
privadas incluídos. Logs build-0.6.14.log/verify-0.6.14.log em
/workspace/striker-runtime. Tamanho 30207473 bytes.
SHA-256: eb9af3189e0a6f835d2ea768051b3cc408f6d0448b19b571ec9d03a03e74111c.

Próximo: validar contador e nome no menu/marcadores no telefone. Validação
física desta versão pendente; sem AAB/assinatura release nesta etapa.

## 0.6.15 — oportunidades dependentes do adversário

Quantidade e probabilidade de oportunidade fácil passam a depender do rating
e posição do adversário na liga dele. Energia/moral mantidas. Perfil definido
ao início do jogo com o adversário correto, em casa ou fora. Adversário muito
forte: no máximo uma oportunidade, sempre difícil; forte: máximo duas, 15% de
atribuir uma fácil; restantes: máximo três, probabilidade fácil até 60% a descer
com a pressão. Zero oportunidades continua possível.
Classificação tem peso gradual até cinco jogos; uma tabela sem jogos não
conta. Elite ou top-15% após cinco jogos força o perfil muito forte. Taças
consultam a liga do adversário; seleções/sem tabela usam apenas rating.
Simulação de resultados, física, treino, UI e progresso existente não alterados.

Ficheiros: career.py, main.py, buildozer.spec, tests/test_career.py,
ui_tests/test_menus.py, AGENTS, README e docs/UI_0.6.15.md. Baseline preservado.
38 testes core/build/segurança + 32 Kivy passaram (70); py_compile e
git diff --check. Novos testes cobrem qualidade/posição, 500 amostras pareadas
fraco/forte, liga própria do adversário de taça, seleções, tabela sem jogos e
integração em casa/fora. Teste genérico de tipos de remate usa perfil fraco
explícito para isolar a regra de no máximo uma chance fácil. Sem falhas novas
na execução. Logs /tmp/scorer-0615-core.log e /tmp/scorer-0615-ui.log.
Sem mudanças visuais; não foram produzidas novas capturas de ecrã nesta etapa.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.15, versionCode 1026615, API 36/mínimo 26.
Assinatura v2 válida com certificado anterior; ZIP e 118 ELF alinhados a 16 KB.
Perfil e uso do adversário confirmados no bytecode empacotado. Sem permissões
declaradas, saves ou chaves privadas incluídos. Logs build-0.6.15.log e
verify-0.6.15.log em /workspace/striker-runtime. Tamanho 30208805 bytes.
SHA-256: f99019b28fe69cb43bd657a6af5c647d59cd98b41378d38da2ba308a1dd3841f.

Próximo: comparar partidas contra líderes, equipas intermédias e fracas no
telefone. Validação física/equilíbrio humano pendentes; sem AAB/assinatura release.

## 0.6.16 — correção de jogos sem oportunidades após treino

Relato: carreira nova com zero chances nos primeiros dois jogos apesar de
3/3 em cada treino. Causa: o sorteio introduzido em 0.6.15 tinha limite inferior
zero, mesmo após treino obrigatório, e os golos do treino só ajudavam por
energia/moral. Corrigido chance_count: treino concluído garante no mínimo
uma oportunidade, incluindo em saves anteriores. Golos da sessão da semana
adicionam 0,15 cada à média (máximo 0,45), sem exceder limites do adversário.
Muito forte mantém exatamente uma oportunidade, sempre difícil. Não altera
física, golos históricos ou classificação; golos do treino não contam na liga.

Ficheiros: career.py, buildozer.spec, tests/test_career.py, ui_tests/test_menus.py,
AGENTS, README e docs/UI_0.6.16.md. Save v2 e baseline preservados.
40 testes core/build/segurança + 33 Kivy passaram (73); py_compile e
git diff --check. Regressão integrada percorre as primeiras duas semanas
com 3/3 em cada treino e abre uma chance em cada partida. Core testa 500
sorteios por força do adversário, treino guardado/recarregado, legado e
efeito do bónus. Sem falhas novas. Logs /tmp/scorer-0616-core.log e
/tmp/scorer-0616-ui.log. Sem alteração visual ou novas capturas nesta etapa.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.16, versionCode 1026616, API 36/mínimo 26.
Assinatura v2 válida com certificado anterior; ZIP e 118 ELF alinhados a 16 KB.
Código do bónus/treino verificado no APK; sem permissões declaradas, saves
ou chaves privadas incluídos. Logs build-0.6.16.log/verify-0.6.16.log em
/workspace/striker-runtime. Tamanho 30208941 bytes.
SHA-256: 9c2e0f6776a1cadefd46ef58ad35d42f599fc1cf456aa31f1531f1f10ad5441b.

Próximo: atualizar sem desinstalar e confirmar oportunidades nas próximas
partidas após treino. Não é preciso recomeçar a carreira. Validação física
desta versão pendente; sem AAB/assinatura release nesta etapa.

## 0.6.17 — investigação e calibração de golos

Investigadas três épocas completas de League Two/Premier League (2022/23–
2024/25) em openfootball/england e duas épocas de remates (2017/18–2018/19)
no espelho público FootballData. Fornecedor direto devolveu 403; usados
repositórios públicos com revisões e hashes fixados. League Two: 4316 golos
em 1656 jogos, média 2,606. Remates: 2867 golos/24377 remates/9373 enquadrados
(~11,76% e ~30,59%). Fontes, distinções e limites em docs/REALISM_0.6.17.md
e docs/data/real_football_reference.json; nenhum pack real/nome oficial no APK.

Auditoria: toque direto permitia repetir cantos quase infalíveis; velocidade
e limite de voo aceleravam remates longos. Ajustada dispersão física de saída
por pressão/condição/potência, velocidade horizontal 18–26 m/s e máximo de voo
1,15 s em jogo; treino conserva comportamento original. GR hard passa a reação
0,14–0,22 s e melhor deslocação. Golos mantêm-se decididos pela física.
Orçamento de golos simulado 1,43/1,18 (total 2,61), dividido por força/posição;
a contribuição esperada do jogador é reservada antes de sortear colegas.
Corrigida dupla atribuição de golos pessoais a NPCs, exclusão de taça da
classificação da liga e uso do contador correto no UI. Distribuição NPC passa
de uniforme a papéis ponderados, sem criar golos extra e com identidade pelo
clube completo. Papéis são hipótese do modelo, não medição dos CSVs.
Progresso e golos históricos preservados; defeitos históricos não reconstruídos
sem dados suficientes. Mínimo de participação após treino e adversários mantidos.

43 testes core/build/segurança + 36 Kivy passaram (79), py_compile e
git diff --check. Novos testes de conservação/taça/reload, orçamento de golos,
papéis, velocidades, dispersão sem resultado pré-determinado, treino intacto e
reserva de golos em casa/fora. Logs /tmp/scorer-0617-core-final.log e
/tmp/scorer-0617-ui-final.log. Não houve falhas de implementação nas suites;
a validação física revelou o limite de voo antigo e motivou repetição dos
ensaios afetados/compilação após a correção. Sem alterações de geometria/arte.

Ensaios reproduzíveis com saves temporários e baseline da3db00 isolada:
- 100 épocas/55200 jogos: 2,720 para 2,620 golos/jogo; 5+ golos 13,97% para
  12,58%; líder de marcadores médio 13,82 para 29,31 com os mesmos golos
  redistribuídos por papéis (não é comparação com jogadores reais).
- 240 remates físicos por perfil/estratégia: canto hard 85,8% para 30,0%;
  canto easy 100% para 48,3%; alvos variados hard 18,3%, easy 50,8%.
- 100 partidas completas com bot instantâneo aos cantos: 3,64 para 2,81
  golos/jogo, 190 para 67 golos pessoais, 28% para 13% jogos com 5+ golos.
  Outros 100 jogos com alvos variados: 2,85 golos/jogo e 37 golos pessoais.
Resultados/condições em docs/data/simulation_0.6.17.json. Bots não são testes
humanos/Android, amostras são limitadas e sequências de épocas divergem.
Ferramentas tools/analyse_football_data.py, calibrate_goals.py,
calibrate_playable.py e balance_shots.py permitem reprodução.

Ficheiros alterados: career.py, main.py, menu_ui.py, buildozer.spec, testes
core/Kivy, ferramentas acima, AGENTS, README e relatório/dados. Baseline imutável
continua fed211d2ec63fe0275390b13ed4a1bcfcd18fa61238460b04b67d80ebca6205b.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.17, versionCode 1026617, API 36/mínimo 26.
Assinatura v2 válida com certificado anterior; ZIP e 118 ELF alinhados a 16 KB.
Código final de golos/voo/dispersão confirmado no APK; arte conferida por bytes.
Sem permissões declaradas, CSVs brutos, saves ou chaves privadas incluídos.
Logs build-0.6.17.log e verify-0.6.17.log em /workspace/striker-runtime.
Tamanho 30210325 bytes. SHA-256: 542314cb93bf31ef0509c6fbf249395aebf37f06d1e9fa884510a625d2d9b5e5.

Próximo: jogar várias partidas no telefone, avaliar justiça da mira e frequência
de golos. Validação física/equilíbrio humano pendentes. Modelo FREE calibrado
para League Two, sem alegar que todas as ligas mundiais foram calibradas.
Sem AAB/assinatura release nesta etapa.

## 0.6.18 — alternância casa/fora no campeonato

Corrigida orientação dos emparelhamentos: antes a paridade da jornada era
aplicada a todos os pares e podia criar longas sequências casa/fora. Versão 2
fixa a paridade por par, alternando o primeiro, e reordena a segunda volta
(inversão com desfasamento de duas jornadas). Cada equipa tem no máximo uma
quebra de alternância por volta, incluindo transição para a segunda; nunca
três jogos seguidos na mesma condição. Adversários uma vez em cada volta com
local invertido; 24 equipas: 46 jogos, 23 casa e 23 fora. Pausas corrigidas para
casos ímpares de teste. Taças conservam sorteio independente.

Novo campo opcional schedule_version no save v2. Saves antigos migram já apenas
se todos os jogos realizados mantiverem adversário/local (normalmente 0–1
jornadas em FREE). Épocas antigas incompatíveis mantêm o calendário inteiro
até terminarem e mudam na época seguinte. Preservados resultados/progresso;
sem pedir novo jogo ou substituir retroativamente jogos realizados.

47 testes core/build/segurança + 37 Kivy passaram (84), py_compile e
git diff --check. Verificação completa de campeonatos com 2–32 equipas, pares
únicos, locais invertidos, contagens iguais, regra por volta/transição e ausência
de triplas. Hashes dos calendários legados 5/24 equipas preservados. Testes de
save/load com 0/1/2 jornadas, histórico/pontos/golos, mudança de época,
recarregamento e rejeição transacional de versão desconhecida. Kivy confirma
o mesmo próximo jogo no calendário, menu e lançamento.
Primeiro teste Kivy herdou viewport minúsculo onde o resumo é ocultado de
propósito; preparação corrigida para 960×540 com cleanup, sem mudar o UI.
A análise inicial da transição entre voltas encontrou uma quebra adicional
para duas equipas; corrigida ordenação da segunda volta e adicionada asserção
que também conta essa fronteira. Logs /tmp/scorer-0618-core-final.log e
/tmp/scorer-0618-ui-final.log. Sem alterações de arte/geometria ou novas capturas.

Ficheiros: career.py, buildozer.spec, testes core/Kivy, AGENTS, README e
docs/UI_0.6.18.md. Baseline preservado (fed211d2ec63fe0275390b13ed4a1bcfcd18fa61238460b04b67d80ebca6205b).
Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.18, versionCode 1026618, API 36/mínimo 26.
Assinatura v2 válida, mesmo certificado; ZIP e 118 ELF alinhados a 16 KB.
Código do calendário/migração confirmado no APK. Sem permissões declaradas,
saves ou chaves privadas incluídos. Logs build-0.6.18.log/verify-0.6.18.log
em /workspace/striker-runtime. Tamanho 30211485 bytes.
SHA-256: 385892f68d4706661128d35160e3e838daee2f0bc82dfe76ec8ce50355a05697.

Próximo: verificar calendário do campeonato em época nova/compatível no telefone.
Época legada incompatível preservada até à seguinte. Validação física desta
versão pendente; sem AAB/assinatura release nesta etapa.

## 0.6.19 — caixa YOUR PLAYER

A partir da captura do proprietário, removida a linha decorativa do painel
que atravessava o campo. Campo do nome arredondado, com contorno de foco e
texto centrado verticalmente. Margens alinhadas, menos espaço vazio e painel
com altura pelo conteúdo. Ajuste compacto de margens/espaçamento mantém
controlos de 52 dp. Sem mudar validação, capitalização, saves ou jogabilidade.

Ficheiros: menu_ui.py, buildozer.spec, AGENTS, README e docs/UI_0.6.19.md.
47 testes core/build/segurança + 37 Kivy passaram (84), py_compile e
git diff --check. Cobertura funcional/layout existente usada nesta alteração
visual: perfil novo/editar, validação, gravação e limites em ecrãs de telefone.
Logs /tmp/scorer-0619-core.log e /tmp/scorer-0619-ui-final.log.
Captura real Kivy scorer-0619-profile0002.png em 1280×589/densidade 1,64
inspecionada. Primeiro ensaio visual mostrou cor do contorno a afetar texto;
adicionado reset de Color e contraste explícito, captura final conferida.
Não é captura Android. Baseline preservado.

Compilação real: bash tools/android/run.sh python tools/build_android.py -v android debug.
APK beta debug arm64 0.6.19, versionCode 1026619, API 36/mínimo 26.
Assinatura v2 válida com certificado anterior; ZIP e 118 ELF alinhados a 16 KB.
Código do campo confirmado no APK; sem permissões declaradas, saves ou chaves
privadas incluídos. Logs build-0.6.19.log/verify-0.6.19.log em
/workspace/striker-runtime. Tamanho 30212625 bytes.
SHA-256: b9ff9b7e011a0f651da9c9181627a84ea64b07ebf62915a25f7cf43b556a825c.

Próximo: atualizar sem desinstalar e verificar caixa/teclado no telefone.
Validação física desta versão pendente; sem AAB/assinatura release nesta etapa.

## 0.6.20 — requested training/balance/presentation revision

Changes/evidence/limits: docs/UI_0.6.20.md; seeded results in
 docs/data/balance_0.6.20.json. Files: career.py, main.py, buildozer.spec,
 tools/balance_shots.py, core/Kivy tests, AGENTS, README and these docs.

49 core/build/security + 38 actual Kivy tests pass (87 total), syntax and
 git diff --check pass. Initial expected-contribution regression correctly failed
 after moving the reserved hard-shot mean from .18 to .20; updated its explicit
 expected totals, reran both suites successfully. Headless desktop lacks optional
 xclip/xsel clipboard executables; Kivy fallback runs, all UI tests pass.

240 seeded uniform attempts/profile before and after: hard 44 -> 49 goals;
 training 131 -> 75; clear unchanged at 122. Corner strategy final hard 97/240.
 100 complete playable matches: 2.46 total goals/match, 59/224 personal shots.
 Desktop scoreboard/catch screenshots rendered and inspected. Not device tests.

Actual build tools/android/run.sh python tools/build_android.py -v android debug
 passed. Signature v2 and existing certificate verified, ZIP16KB and 118 ELF
 alignments pass. Actual package versionCode1026620, target36/min26, no requested
 permissions. Payload inspected for saves/signing keys. APK30,215,905 bytes,
 SHA256 d2d938c1f8331a81db65f037b652a65c1632b8a4ad8282932a67bd4a1f008114.
 Logs build-0.6.20.log and verify-0.6.20.log in /workspace/striker-runtime.
 Next: actual phone training, hard shots, keeper catch/fall, scoreboard and flags.

## 0.6.21 — complete fixtures and progressive cup draws

Changes: docs/UI_0.6.21.md. Files: career.py, menu_ui.py, buildozer.spec,
core/Kivy tests, AGENTS, README and docs. 51 core/build/security tests and
38 real Kivy tests pass (89). Syntax/whitespace and baseline hash pass.
An initial UI regression from calling the removed detail view was fixed by
a safe no-op for tables without details; all UI tests rerun successfully.
Full schedule and 35-result persistence/reload tested; cup draws stable through
all eight rounds/final with no repeated eliminated opponent.

Actual Android build: build-0.6.21-final.log. Static verification: signature v2
with existing debug certificate, ZIP16KB and all 118 AArch64 ELF alignments,
package com.clemir.striker/versionCode1026621, target36/min26, no permissions.
Payload checked: no saves or signing keys. verify-0.6.21.log retained outsideGit.
APK 30217021 bytes, SHA256 77e8f0c8ce4e3c842ecb101164cd5ff381c251efbc3f575808d48a992043713b.
Desktop fixtures screenshot inspected; current APK not tested on a phone.
Next: phone fixture pages, save/load, cup progression and weekly training.

## 0.6.22 — AdMob native SDK, TEST only

Owner supersedes no-AdMob restriction by requesting immediate network revenue;
no account exists, general audience includes minors. Real production revenue is
blocked by account/IDs/readiness, not represented as achieved. Full instructions
and data/permission implications: docs/ADMOB_SETUP.md. Implementation/evidence:
docs/UI_0.6.22.md. Added advertising.py, Java ScorerAds bridge, manifest removals,
Gradle SDK pins, main/menu hooks, controller and actual Kivy integration tests.

56 core/build/security and 41 actual Kivy tests pass (97). Early failures: exact
menu counts changed by Privacy; new test had not loaded its career. Corrected
expectations/setup, retained geometry/overlap assertions, reran full suites.
Syntax, git whitespace and immutable baseline checks pass. Real desktop entry,
hub and privacy screenshots inspected. No actual Android ad has been displayed.

Actual Android build build-0.6.22-banner.log successful, GMA25.5.0/UMP4.0.0 and Java
bridge in DEX verified. APK version1026622, target36/min26, same debug signaturev2,
ZIP16KB + 118 AArch64 ELF alignments pass. Manifest sample App ID and DEX official
TEST ad unit checked. AD_ID and all three AdServices permissions absent; network,
wake-lock, foreground-service and AndroidX signature receiver permissions remain.
No saves/private keys in APK. APK37,175,750 bytes,
SHA256 28b4abdaf13cebdb3a75df32c895c352366b416d4ae6058f5be705db2ff75cc7.
Native presentation/UMP/rotation/offline/performance still need phone validation.
No production IDs, no payments, no Play publishing, no revenue claimed.

Owner additionally requests ads after splash: added native TEST banner in the
entry menu only, separate 64dp footer and safe-size suppression. Removed on
navigation, never delays splash/menu or appears during play. Controller visibility
transitions and actual Kivy button/footer separation added to the passing suite.

## 0.6.23 — first post-match ad and optional morale RewardedAd

Owner reports 0.6.22 banner displayed, no post-match ad. Old 3-match/180s gate
can explain this, no device error log available. First final CONTINUE now eligible
if ready, subsequent fullscreen minimum60s. Prefetch earlier and separate Privacy
status for break/reward failures. Optional training +1 morale capped20/once-weekly,
SDK earned callback only, native private receipt, atomic save + idempotent ack.
Files/evidence: docs/UI_0.6.23.md; four production IDs needed in ADMOB_SETUP.md.

59 core/build/security and 42 real Kivy tests pass (101). Includes save failure,
replay/reload, stale contexts, no reward on request/early close without SDK record,
first-match/cooldown and existing full suites. Initial UI caught 8px overflow;
compacted training spacing/removed duplicated energy line, all UI rerun passed.
Desktop training capture at density1.64 inspected. Actual 0.6.23 ad load/show/earned
callback/rotation/early close still need Android phone validation.

Real build build-0.6.23-final.log successful. SDK RewardedAd/receipt and all TEST
IDs in DEX verified, Python advertising.pyc in payload; no saves/private keys.
Same debug signaturev2, package com.clemir.striker/version1026623, target36/min26,
ZIP16KB +118 AArch64 ELF alignments pass, AD_ID/AdServices permissions still absent.
APK37,181,442 bytes, SHA256
5477d0272298ae493294f22cf40bf83c64eaffc338e9618043840b5715754dcd.
Static log verify-0.6.23.log; no production revenue or paid IDs activated.

## 0.6.24 — Help, locale starts, World test edition and names editor

Full change/test/build/limitation report and hashes: docs/WORLD_0.6.24.md.
67 core/build/security +44 actual Kivy tests pass (111), syntax/whitespace and
baseline hash pass. New coverage: locale/one Free division, World table reload,
World access not save-unlockable, alias import/rollback/UID/scorer preservation,
same-name cross-country isolation, promotion swap and all cup rounds before
short-league season end; Help/Upgrade/navigation/editor and prior layout suite.

Initial UI action-count expectations updated from9 to11, preserving geometry/
48dp targets. Audited/fixed original promotion duplication and local Free season
switch-to-England hazard. Aliases originally used ambiguous global name matching;
now direct UID/country context with regression. Compacted initial contracts/editor
after real desktop screenshots showed avoidable scrolling. No physical phone test
of the new edition/SAF/companion launch yet. World simplified international model
and fictional pyramids explicitly documented; no paid release claimed.

Two actual final builds successful, Free com.clemir.striker and World test
com.clemir.strikerworld.preview. World distribution first failed due to mixed
packaging pip files; preserved/recreated disposable venv, native caches retained.
Both signaturesv2 (same prior certificate), ZIP16KB and 118 ELF alignment checks
pass, target36/min26/version1026624. Compiled edition.pyc flags checked using
built hostPython3.14: Free false, World true. World DEX LocalNameFiles present,
Google Ads absent, no Internet/Billing permission. Free AdMob TEST remains, no
Billing/AD_ID/AdServices. No private saves/keys in either private archive.
Logs: build-0.6.24-{free,world}-final.log / verify-0.6.24-{free,world}.log.
Next: install alongside Free, test locale/English contracts, Help/Upgrade, World
season/transfer, document export/import and alias persistence on Android.
