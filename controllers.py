from AIGamePyLibrary.AIGamePyLibrary import *

from mode_selector import BALL_INCOMING, SERVING, AWAITING_SERVE, RECEIVING, AWAITING_HIT, BALL_OUT
from params import SERVE_SIDE_FLOAT, SIDE_FLOAT
from score_targets import AIM_TARGET, SHOT_TYPE
from trajectory_predicter import INTERCEPT_POINT, INTERCEPT_TIME
from move_controllers import (
    awaiting_hit_move_controller,
    awaiting_serve_move_controller,
    serving_move_controller
)
from swing_controllers import (
    serving_swing_controller,
    receiving_swing_controller
)
from aim_controllers import serve_aim_controller
from utils import plot_bool, squash_y_axis
def move_controller():
    awaiting_hit_move = ConditionalSetVector3(
        AWAITING_HIT,
        awaiting_hit_move_controller(),
        TennisGetVector3("Center Of Half")
    )

    receiving_move = ConditionalSetVector3(
        CompareBool(RECEIVING, Not(BALL_OUT)),
        INTERCEPT_POINT,
        awaiting_hit_move
    )

    awaiting_serve_move = ConditionalSetVector3(
        AWAITING_SERVE,
        awaiting_serve_move_controller(),
        receiving_move
    )

    serving_move = ConditionalSetVector3(
        SERVING,
        serving_move_controller(),
        awaiting_serve_move
    )

    return serving_move

def aim_controller():
    aim_target = ConditionalSetVector3(
        SERVING,
        serve_aim_controller(),
        AIM_TARGET
    )

    return aim_target

def swing_controller():
    serving_swing = ConditionalSetBool(
        SERVING,
        serving_swing_controller(),
        receiving_swing_controller()
    )
    return serving_swing

def shot_controller():
    serve_shot = ConditionalSetFloat(
        (SERVE_SIDE_FLOAT * SIDE_FLOAT) > 0.0,
        TennisGetFloat("Shot: Curve Left"),
        TennisGetFloat("Shot: Curve Right")
    )
    return ConditionalSetFloat(
        SERVING,
        serve_shot,
        SHOT_TYPE
    )

def sprint_controller():
    move_target = move_controller()
    player_position = RelativePosition(TennisGetTransform("Self"), "Self")

    player_distance_to_target = Magnitude(
        squash_y_axis(SubtractVector3(move_target, player_position))
    )

    needed_speed = DivideFloats(player_distance_to_target, INTERCEPT_TIME)

    sprint = CompareBool(BALL_INCOMING, CompareBool(needed_speed > 7, needed_speed <= 13.7))
    give_up = needed_speed > 13.7

    return sprint, give_up