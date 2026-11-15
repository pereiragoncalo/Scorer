"""The unchanged Scorer 1 lateral perspective, also used by the net lab."""
from career import CAMERA_POSITION,CAMERA_FORWARD,CAMERA_RIGHT,CAMERA_UP

def project_point(x,y,z,center_x,center_y,focal):
    dx,dy,dz=x-CAMERA_POSITION[0],y-CAMERA_POSITION[1],z-CAMERA_POSITION[2]
    depth=max(.05,dx*CAMERA_FORWARD[0]+dy*CAMERA_FORWARD[1]+dz*CAMERA_FORWARD[2])
    return (center_x+focal*(dx*CAMERA_RIGHT[0]+dy*CAMERA_RIGHT[1]+dz*CAMERA_RIGHT[2])/depth,
            center_y+focal*(dx*CAMERA_UP[0]+dy*CAMERA_UP[1]+dz*CAMERA_UP[2])/depth)
