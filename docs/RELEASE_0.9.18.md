# Scorer World 0.9.18 — English default and compact screens

World DEBUG QA upgrade; install over the existing World QA and choose Load Game.
The existing package, career saves and DEBUG upgrade certificate are preserved.
Public version 1.0 remains separate.

English is the initial language irrespective of the phone language. Explicitly
saved language selections remain available. Legacy automatic preferences migrate
to English; newly selected Automatic persists using preference schema 2. Phone
country detection still controls suggested starting contracts independently.

The launch notice uses a centred compact panel and readable 12sp justified text,
with fixed agreement/exit buttons and overflow scrolling on very small windows.
The automatic collection and destination disclosure remains visible before
agreement; no collection behaviour or public policy was altered.

Help contains gameplay instructions, with justified paragraphs and no privacy
rules. The existing Settings link retains access to career transfer. Training instructions now correctly require three shots
before every match. World help explains World > Editor and JSON name imports.
All nine language catalogues include the new World instructions.

The coach meeting's final paragraph is justified across the full panel width,
starting below the portrait and the preceding feedback. The measured full/short
variants retain three feedback parts, a reachable completion button and a single
screen without scrolling or pagination.

Validation: 354 core tests, 168 native Kivy tests and 891 responsive audit cases
(27 views, 11 size/density/font configurations, Portuguese/German/Japanese).
The audit found no bounds, touch-size, measured text-height or one-screen
findings. Representative English notice and coach screens were inspected visually.
APK checks cover exact compiled source/data, World edition, competitions,
release payload, package/version, signing, API levels and 16KB alignment.

This is desktop native-layout verification and an installable DEBUG QA build;
physical Android installation/handset checks remain pending. It is not a Play
production upload or approval.
