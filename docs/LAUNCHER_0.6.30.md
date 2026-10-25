# SCORER 0.6.30 — Android launcher identity

The owner requested separate launcher entries named Scorer and Scorer World.

| APK | Launcher label | Package | Launcher art |
| --- | --- | --- | --- |
| Free | Scorer | com.clemir.striker | Original emerald/gold S, assets/icon.png |
| World | Scorer World | com.clemir.scorerworld | Blue globe, gold S and WORLD, assets/icon_world.png |

Both APKs must be installed for both entries to appear. Each launches its own
application with its own private career. Package IDs and existing debug signing
certificate remain unchanged;0.6.30/code1026630 upgrades the respective0.6.29
installation without uninstalling. No additional launcher aliases or cross-app
installer/package-query permissions were added. Free remains English-only;
World retains all nine languages and no advertising SDK. Existing UI wordmarks
and the touch-to-dismiss splash are unchanged.

Changes: buildozer.spec default Free label/version, tools/prepare_editions.py
per-product label/icon/version and stripping the World icon from Free, main.py
window title matching launcher labels, assets/icon_world.png, assertions in the
existing product-staging regression test, and release documentation. No gameplay,
career/schema, SDK, payment or country-format change. World art was generated as
a companion to the project's existing S icon; source remains unchanged.

Validation: syntax checks,118 core/security and61 Kivy interface tests (179 total).
Both real arm64 debug APKs compiled sequentially. Actual APK label, launcher icon,
package/version and signature/content checks plus ZIP16KB/118 ELF alignment
checks perAPK are recorded in LAUNCHER_0.6.30_artifacts.json. Existing certificate
SHA256:84c17cdf31e2ee7c6e9c082bde539df6822bf48267a0603de9814d6e2846ef49.

Logs: /workspace/striker-runtime/icons-core.log, icons-ui.log,
build-0630-free.log, build-0630-world.log. Exact source was staged from the tested
snapshot; unrelated unfinished World tournament changes remain preserved.

Phone checks still required: install both APKs; verify two app-drawer entries and
distinct icons/labels; open/save/reload each career independently; confirm upgrades
retain progress. Some launchers do not automatically add installed apps to the home
screen: if needed drag both entries from the app drawer. Old pinned shortcuts may
retain cached artwork until recreated. No physical launcher test or Play upload
was performed here. These are QA/debug builds, not production signed releases.
