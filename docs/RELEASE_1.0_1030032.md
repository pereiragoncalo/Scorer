# Scorer World 1.0 (1030032)

Every ground above10,000 capacity now has an original retro roof/fascia sprite
canopy, including the curved corner. A low55cm wall fronts the first seating
row in all grounds, including open small grounds and empty training venues.
The inclined two-deck canopy keeps its front visible in the existing camera;
stand/player/spectator coordinates and sizes remain unchanged.

The club screen shows a palette-recoloured retro stadium picture beside factual
information. Six original320x180 variants follow capacity:≤5k,≤10k,≤25k,≤40k,
≤80k and above80k. Two-deck variants match the existing >40k ground model.
Unknown factual capacities remain unavailable; art uses the same bounded venue
model already used in play. Existing factual profiles and names are unchanged.
All art is original and reproducible from tools/build_stadium_sprites.py.
Pillow is build-time only; runtime uses nearest sampling and bounded texture
caches. Architecture is five small cached material batches, no gameplay RNG.

Seven capacity/profile/resource checks and20native journeys pass, including the
exact10k boundary,150k roof framing, away host/own training venue, empty training,
cache allocations, RNG/ball preservation, portrait layout at640x295/1280x720,
club navigation and previous net restoration. Native open/covered/large/club
screenshots reviewed. Physical Android acceptance remains pending.
No save/physics/financial/backend/signing changes. Update without uninstalling.
Keep minimum1030031 until Play offers1030032 to every intended player.
Commands: docs/play/FIXES_1030032.md.
