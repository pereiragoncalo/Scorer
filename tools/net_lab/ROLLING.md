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
