from AIGamePyLibrary.AIGamePyLibrary import *
from params import SIDE_FLOAT, SERVE_SIDE_FLOAT

def awaiting_hit_move_controller():
    center_half = TennisGetVector3("Center Of Half")
    center_back = TennisGetVector3("Center Of Back")
    b2h_vec = center_half-center_back

    opponent_pos = RelativePosition(TennisGetTransform("Opponent"), "Self")
    _, _, opponent_z = Vector3Split(opponent_pos)

    return center_back + b2h_vec * 1.6 + Vector3(0,0,opponent_z*0.1)

def awaiting_serve_move_controller():
    receive_pos = TennisGetVector3("Receive Stance")

    return receive_pos

def serving_move_controller():
    return TennisGetVector3("Center Of Back") + Vector3(0,0,-6)*SERVE_SIDE_FLOAT*SIDE_FLOAT
