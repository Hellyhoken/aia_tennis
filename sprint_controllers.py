from AIGamePyLibrary.AIGamePyLibrary import *

from utils import squash_y_axis

def sprint_info():



    move_target = GetVariable("move")
    player_distance_to_target = Distance(squash_y_axis(RelativePosition(TennisGetTransform("Self"),"Self")),squash_y_axis(move_target))
    ball_x_vel,_,ball_z_vel = Vector3Split(TennisGetVector3("Ball velocity"))

    ball_speed = Operation(AddFloats(Power(ball_x_vel,2),Power(ball_z_vel,2)),"sqrt")

    ball_distance_to_target = Distance(squash_y_axis(TennisGetVector3("Ball position")),squash_y_axis(move_target))
    
    time = DivideFloats(ball_distance_to_target, ball_speed)

    needed_speed = DivideFloats(player_distance_to_target,time)

    return CompareBool(needed_speed>8,needed_speed<=13,"and"),needed_speed>13
    



    


