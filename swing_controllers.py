from AIGamePyLibrary.AIGamePyLibrary import *

def serving_swing_controller():
    charge_pct = TennisGetFloat("Self Swing Charge Pct")
    charged = charge_pct > 0.75

    racket_transform = TennisGetTransform("Self Racket Center")
    racket_positon = RelativePosition(racket_transform, "Self")
    ball_position = TennisGetVector3("Ball Position")
    racket_distance = Distance(racket_positon, ball_position)

    return CompareBool(charged, racket_distance < 0.3, "nand")


def receiving_swing_controller():
    move_target = GetVariable("move")
    move_x, _, _ = Vector3Split(move_target)

    ball_position = TennisGetVector3("Ball Position")
    ball_x, _, _ = Vector3Split(ball_position)

    ball_velocity = TennisGetVector3("Ball Velocity")
    ball_vx, _, _ = Vector3Split(ball_velocity)

    x_dist = Abs(ball_x - move_x)
    ball_arrival_time = x_dist / ball_vx

    should_charge = ball_arrival_time < 0.82
    should_hit = x_dist < 0.3

    return CompareBool(should_charge, ~should_hit, "and")
