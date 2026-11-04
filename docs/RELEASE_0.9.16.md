# Scorer World0.9.16 — more duels, announced penalties and one-screen reading

World DEBUG QA upgrade; install over existing World QA and Load Game. Package,
saves, upload-free name imports and existing DEBUG certificate are retained.
Public1.0 remains separate; no Play upload, production signing or server change.

Clear opportunities are more frequent: probability0.35 against elite opponents,
0.65 at medium pressure and roughly0.73–0.90 below that. The existing cap of one
clear chance and maximum three total chances remain. Clear shots favour kicks
90%/headers10%, and have no outfield defenders or teammates. Hard shots retain
defenders. Penalties are selected before the opportunity notice, with18% chance
in a match that has personal opportunities, replacing an existing chance. They
avoid the clear-chance slot when another slot exists. The notice explicitly says
“You have been chosen to take the penalty.” The shot starts at0,11m against only
the keeper. Training stays three normal finishing shots without penalties.

The personal-goal reservation now includes the modeled penalty contribution
(0.65 conversion, not a measured human rate), subtracting the clear/penalty overlap
when there is only one chance. AI team means remain the existing model; no goals,
misses or personal-goal quotas are forced. Actual shot/keeper physics are retained.

The newspaper now always has one leaf and no Next/Previous controls or scroll.
Full prose is used when it fits; otherwise a concise edition retains the result,
every recorded home/away goal minute, brief margin/draw summary and personal
verdict. Small headers abbreviate club names, keeping full names in the report
model. The image/caption adapt to available space; the decorative image can be
omitted in extreme tiny/high-scoring stress cases. Ordinary phone examples retain
the embedded image and full four-goal report. A minimum6sp was exercised
in the320×240/64-goal stress case; this is not a universal readability claim.
No hidden leaves or silently dropped goal minutes are used.

Coach meetings use a dedicated screen with portrait and a fixed completion
button. Measured type selects full or concise three-paragraph feedback. Compact
screens place the portrait in the header and retain three substantive feedback
parts. There is no ScrollView. Tested body fonts are9sp or above; normal phone
previews use larger full feedback. Requested-meeting and saved post-match order
remain unchanged.

The launch-notice paragraph is justified; notice content/agreement are unchanged.
The first delivered splash touch is handled directly by the game root, including
before child layout has completed. This addresses a swallowed first app touch;
OS/native-loading/focus behaviour still needs a physical handset check.

Player navigation moves to the existing name position: the name is now the
button. The three World header actions align exactly to the right season panel.
The name button keeps a52dp target. The hub rebuilds when its viewport changes,
fixing a compact startup layout that could persist until another state change.
Other views retain their widgets on resize, preserving profile input drafts.

Validation:353 core +165 native Kivy tests (518 total), plus final targeted
layout/locale/resize checks. New cases cover penalty preannouncement/origin,
more clear chances, budget conservation, first splash touch before layout,
justified notice, name navigation/header bounds, nine-language one-screen
news/coach, all64 goal minutes, startup resize and profile draft retention.
Initial full runs caught old elite/leaf/PLAYER expectations, a stale header
callback, caption overlap and a36dp identity row; these were corrected before the
final build. Exact compiled gameplay/UI/coach modules and all nine catalogue bytes
are verified, with API36/min26, arm64,118ELF/ZIP16KB and ad-free payload checks.

Five Portuguese previews are real desktop Kivy renders at1280×591/density1.4,
using synthetic fixture/stats data. They are not physical Android screenshots.
Physical Android validation remains outstanding, especially the reported splash
first-touch behaviour.
