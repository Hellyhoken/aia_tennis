from AIGamePyLibrary.AIGamePyLibrary import *

from utils import plot_bool

def serving_swing_controller():
    charge_pct = TennisGetFloat("Self Swing Charge Pct")
    charged = charge_pct > 0.65

    return ~charged


def receiving_swing_controller():
    move_target = GetVariable("move")
    racket_offset = GetVariable("racket_offset")
    racket_target = AddVector3(move_target, racket_offset)
    racket_x, _, _ = Vector3Split(racket_target)

    ball_position = TennisGetVector3("Ball Position")
    ball_x, _, _ = Vector3Split(ball_position)

    ball_velocity = TennisGetVector3("Ball Velocity")
    ball_vx, _, _ = Vector3Split(ball_velocity)

    x_dist = Abs(ball_x - racket_x)
    ball_arrival_time = Abs(x_dist / ball_vx)

    at_thresh = 0.95
    hit_thresh = 0.05

    arrival_time_ts = TimePlot("arrival time", "Blue", "", ball_arrival_time)
    arrival_thresh_ts = TimePlot("arrival time threshold", "Green", "", at_thresh)
    x_thresh_ts = TimePlot("0.3", "Red", "", hit_thresh)

    should_charge = ball_arrival_time < at_thresh
    should_hit = ball_arrival_time < hit_thresh

    return CompareBool(should_charge, ~should_hit, "and")
