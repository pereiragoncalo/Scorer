# Original retro stadium art

Nine original RGBA pixel assets authored by `tools/build_stadium_sprites.py`.
Pillow is a build-time authoring tool only; runtime uses cached Kivy textures
with nearest sampling. No external stadium photographs or logos are copied.

The six 320×180 club pictures represent capacity bands: local ≤5,000;
compact ≤10,000; covered ≤25,000; bowl ≤40,000; double ≤80,000; major above.
Grounds above 10,000 have roofs. Both higher bands show two decks, consistent
with the in-game ground model. They are illustrations, not factual venue plans.

The 128×32 roof and 128×16 fascia/wall are mapped to cached scene quads.
RGB(40,80,210) and RGB(240,240,220) are the existing runtime club-colour slots.
The smaller props use neutral metal/concrete shading around these accents.
