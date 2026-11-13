"""The unchanged Scorer 1 lateral perspective, also used by the net lab."""
from career import CAMERA_POSITION,CAMERA_FORWARD,CAMERA_RIGHT,CAMERA_UP,dot3

def project_point(x,y,z,center_x,center_y,focal):
    relative=(x-CAMERA_POSITION[0],y-CAMERA_POSITION[1],z-CAMERA_POSITION[2])
    depth=max(.05,dot3(relative,CAMERA_FORWARD))
    return (center_x+focal*dot3(relative,CAMERA_RIGHT)/depth,
            center_y+focal*dot3(relative,CAMERA_UP)/depth)
