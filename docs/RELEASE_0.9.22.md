# Scorer World 0.9.22 — Scorer Retro throughout the game

The approved retro lettering is now a real bundled TrueType font, used for game
text, buttons, scores, editable fields, popups, the newspaper and coach feedback.
It includes distinct lowercase/uppercase, monospaced digits, punctuation and Latin
accents (645 characters). Existing native-script fonts cover unsupported scripts,
including Chinese, Japanese and Korean; stored names/case/translations are intact.

The splash artwork and original overlay fonts are preserved. The main-menu logo
remains its existing image. Other screen titles use Scorer Retro. The font is
original lettering with licensed Barlow symbols; its OFL attribution and build
source ship in the repository. Runtime needs no font-building dependencies.

Very small coach screens use tighter header spacing and measured text sizing to
keep all three feedback paragraphs, portrait and completion button on one screen.
The full-size screens retain their existing layout. No gameplay, save schema,
training, shots, competitions, stats collection or server settings changed.

This is a DEBUG QA upgrade using the existing package and certificate. Install
over the previous World QA and select Load Game. Public 1.0 remains unchanged.
Physical Android installation and playtesting remain pending.

Validation: 373 core and 179 native Kivy tests passed (552 total). The final
responsive report covers 28 views, 11 resolution/density/font configurations and
Portuguese/German/Japanese: 924 cases, zero findings. All nine languages are also
covered by the tiny newspaper/coach tests. Actual native menu, player, training,
help, newspaper and coach previews were inspected.

Actual APK verification passed: exact compiled modules and font/artwork bytes,
competition/progression/save/edition/safety smoke checks, unchanged DEBUG upgrade
certificate, API36/arm64, and 118 native ELF libraries plus ZIP alignment at16KB.
The initial APK smoke test still expected the retired newspaper face; updated its
assertion to Scorer Retro and reran the full candidate checks successfully.
