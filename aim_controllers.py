from AIGamePyLibrary.AIGamePyLibrary import *

from params import SERVE_SIDE_FLOAT, SIDE_FLOAT, SERVE_OFFSET

#Legal ball positions
#0,0,-6
#0,0,6
#14,0,6
#14,0,-6

def serve_aim_controller():
    serve_offset = SERVE_OFFSET * SIDE_FLOAT
    serve_offset = Vector3(serve_offset.x, 0, serve_offset.z*SERVE_SIDE_FLOAT)

    serve_pos = TennisGetVector3("Legal Serve Target") + serve_offset
    return serve_pos


