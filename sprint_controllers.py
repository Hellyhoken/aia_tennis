from AIGamePyLibrary.AIGamePyLibrary import *

from utils import squash_y_axis

def sprint_info():
    move_target = GetVariable("move")
    player_position = RelativePosition(TennisGetTransform("Self"), "Self")
    player_distance_to_target = Magnitude(
        squash_y_axis(SubtractVector3(move_target,player_position))
    )

    ball_arrival_time = GetVariable("ball_target_arrival_time")

    needed_speed = DivideFloats(player_distance_to_target, ball_arrival_time)

    return CompareBool(needed_speed>8, needed_speed<=14,"and"), needed_speed>14
