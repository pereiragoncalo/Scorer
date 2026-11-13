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
