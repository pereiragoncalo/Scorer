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

Taut installation keeps the lower rail fixed; the slack installation lets the
lower hem gather/slide on the turf while retaining mouth posts, top supports and
rear centre ground peg. Contact effective mass represents the larger cord region
engaged by a taut installation, not the literal mass of a single mesh vertex.
These are qualitative development settings, not measurements of real net types.

Only tools/net_lab/rolling_contact.py and rolling_demo.py implement this experiment.
The production net modules and the version1030017 package remain untouched.
