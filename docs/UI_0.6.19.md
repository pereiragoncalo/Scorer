# SCORER 0.6.19 — player name panel

Corrected the YOUR PLAYER panel shown in the owner's screenshot. Removed the
panel's decorative line, gave the input rounded corners and a dedicated focus
outline, and centred text vertically. Explicit canvas colour reset prevents
the outline colour from tinting the text. Hint text is readable. Panel corners
are softer, inner margins align, and helper height is fixed to content needs
rather than expanding into a large empty gap. Compact screens use smaller
padding/spacing while retaining 52 dp controls.

No player-name validation, capitalisation, career, calendar or gameplay change.
Files: menu_ui.py, buildozer.spec, AGENTS.md, README.md and documentation.

47 core/build/security and 37 real Kivy tests passed (84), including profile
creation/editing, validation, save persistence and phone layout bounds.
py_compile and git diff --check passed. Existing functional/layout coverage
was used for this visual change. A real Kivy capture at 1280×589/density 1.64
was inspected against the supplied screenshot. Initial visual inspection
exposed outline-colour leakage into the hint; reset the canvas colour and
verified the final capture. This is not an Android screenshot.

Actual APK checks are in BUILD_LOG. Next: update without uninstalling and
check this panel and the keyboard on the phone. Physical validation of this
beta remains pending; no AAB or store release signing in this step.
