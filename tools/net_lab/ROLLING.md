# Rolling-contact visual experiment only

Owner requested new simulations only: no game build, signing, upload, version
change or production integration. Run from the existing Scorer Python/Kivy env:

    python tools/net_lab/rolling_demo.py --capture /tmp/rolling --frames 300
    python tools/net_lab/rolling_demo.py --capture /tmp/rolling-slow --frames 600 --playback .5

Both panels start with the exact same rolling sphere position and velocity. The
sphere transfers contact impulses to the existing Verlet mesh, moves along the
side into the side/back junction, and loses momentum through net damping/contact
friction and turf rolling resistance. Position stabilization does not replace the
velocity impulse calculation. The ball is not attached to a fixed UV coordinate.
Atlas spin follows signed distance travelled and stops with the ball.

Every vertex touching the turf is fixed in both installations. Positions and
previous positions stay exactly at their rest coordinates throughout contact.
Sag and deformation occur only in the suspended mesh. Contact effective mass
represents the larger cord region engaged by a taut installation, not the literal
mass of a single mesh vertex.
These are qualitative development settings, not measurements of real net types.

Only tools/net_lab/rolling_contact.py and rolling_demo.py implement this experiment.
The production net modules and the version1030017 package remain untouched.

## Height / speed matrix (simulation only)

    python tools/net_lab/rolling_demo.py --matrix square --capture /tmp/matrix-square --frames 240 --playback .5
    python tools/net_lab/rolling_demo.py --matrix hexagon --capture /tmp/matrix-hexagon --frames 240 --playback .5

Each video shows nine independent replays: target back-net contact heights .22,
1.10 and 2.05 metres (rows), launch speeds 4, 9 and 18 m/s (columns). Launches
start inside the goal, .90 m before the rear sheet; gravity and vertical contact
impulses are enabled. The sagged profile uses .45 slack (previous slack profile:
.38). All turf-contact vertices remain fixed. The square and hexagonal drawings
use the same continuum cloth solver and material parameters so the comparison
isolates mesh appearance; it does not model different cord-level tensile
properties for the two knitting patterns. Videos play at 50% speed.

### Flexible rear ties / deeper pockets

The `sagged` experiment now adds extra hanging fabric between boundary supports,
allows larger link extension and uses softer wave transmission. The three rear
upper support particles are elastic rather than hard pins. Each tie has an
immutable pole endpoint and a net endpoint with at most 12 cm yield; a stiff
restoring spring returns that attachment. Turf-contact vertices and the front
frame remain exact hard pins. The renderer connects each fixed pole endpoint to
the actual moving cloth particle, marking the fixed end in amber. Interior
fabric may deform much further than the ties. This is a qualitative soft-tie
constraint model, not a separate rope-particle simulation.

Updated captures are in `docs/data/net_flexible_ties/`. No production module,
Android version, save or game asset changes are involved.

### Broad folded pocket from the supplied 1990 match stills

    python tools/net_lab/rolling_demo.py --reference --capture /tmp/reference-compare --frames 360 --playback .5
    python tools/net_lab/rolling_demo.py --reference --matrix square --capture /tmp/reference-square --frames 360 --playback .5
    python tools/net_lab/rolling_demo.py --reference --matrix hexagon --capture /tmp/reference-hexagon --frames 360 --playback .5

The reference profile hangs more fabric between the same hard front/turf pins
and compliant rear ties. A smooth finite load footprint (80 cm scale, cut off at
1.2 m) distributes contact over neighboring welded cloth vertices, including
both sheets at the side/back seam. The impulse is normalized over that support;
it is not independently duplicated at every vertex. Contact still samples the
local sheet for penetration; broad support is a development approximation to
force transfer through the loose fabric. Smaller allowed link extension and
stronger tension propagation reduce the narrow, locally stretched spike.

The before/after uses identical initial ball state (12 m/s, .90 m target height),
fixed external tie endpoints and grounded boundaries. More vertices move, rather
than just increasing peak displacement. A regression checks that a fast mid-net
shot moves at least 1.8 times as many vertices by 15 cm as the previous profile.
The square/hexagonal grids still share one continuum material model. The stills
provide shape references, not measured force, timing or damping calibration.
Artifacts are in `docs/data/net_reference_drape/`. These are simulations only.

### Single hard, mid-height shot against the side first

    python tools/net_lab/rolling_demo.py --side-shot --capture /tmp/strong-side --frames 360 --playback .5

One hexagonal reference net, initial velocity (-6,-18,0) m/s (68 km/h), enters
near the left post at mid height. Verified first side contact at .125 s, rear
contact at .192 s, then descent and rolling to rest inside the goal. Base pins
and rear tie limits are unchanged. The video uses 50% playback and has no game
build or integration side effects.

### World 1030018 integration

After owner approval, the same solver moved to root `net_drape.py`. This lab
module is now a compatibility import of that implementation. `net_presentation`
uses a separate read-only-to-game-state display sphere after a legal goal. The
lab UI/presets/capture files remain excluded from the Android package. Earlier
simulation-only notes above describe those earlier deliveries, not this release.

### Unloaded side-pocket correction

    python tools/net_lab/rolling_demo.py --rest-compare --capture /tmp/rest-compare --frames 450 --playback .5

Left shows 1030018's previous stacked outward rest offsets; right shows the new
single downward-only rest field. First 90 frames show unloaded nets without a
ball, then the same side-first shot. Preview: `docs/data/net_rest_shape/`.

### Local contact follows the ball

Following handset feedback after1030019, contact correction and momentum now
use the same four local interpolation weights. The wide radius load footprint
is removed; only the touched strands receive direct loading, with movement
spreading through connected springs. A stationary sphere's overlap cannot push
cloth outward. Old horizontal-only stop markers no longer freeze a ball in the
air. See `docs/data/season_review_contact/rede-contacto.mp4`. No new Android build
has yet been made for this correction.
