from AIGamePyLibrary.AIGamePyLibrary import *

from utils import squash_y_axis

def serving_swing_controller():
    charge_pct = TennisGetFloat("Self Swing Charge Pct")
    charged = charge_pct > 0.65

    return ~charged


def receiving_swing_controller():
    side_constant = ConditionalSetFloat(
        TennisGetBool("Is Home"),
        -1,
        1
    )

    move_target = GetVariable("move")
    ball_position = TennisGetVector3("Ball Position")
    ball_velocity = TennisGetVector3("Ball Velocity")

    horizontal_dist = Magnitude(squash_y_axis(SubtractVector3(move_target, ball_position)))
    horizontal_vel = Magnitude(squash_y_axis(ball_velocity))

    arrival_time = horizontal_dist / horizontal_vel
    at_var = SetVariable("ball_target_arrival_time", arrival_time)
    
    player_trans = TennisGetTransform("Self")
    player_pos = RelativePosition(player_trans, "Self")

    next_step_ball_pos = ball_position + ball_velocity * 0.065 # 0.019 timestep (0.065 to account for swing delay)

    next_player_distance = Distance(player_pos, next_step_ball_pos)
    in_range = next_player_distance < 4

    racket_x_offset = 0.55 * side_constant

    racket1 = player_pos + Vector3(racket_x_offset, 0, 0.45)
    racket2 = player_pos + Vector3(racket_x_offset, 0, -0.45)

    racket1_dist = Magnitude(squash_y_axis(racket1-next_step_ball_pos))
    racket2_dist = Magnitude(squash_y_axis(racket2-next_step_ball_pos))

    player_x, _, _ = Vector3Split(player_pos)
    racket_x = player_x + racket_x_offset
    next_ball_x, _, _ = Vector3Split(next_step_ball_pos)

    x_dist = (racket_x - next_ball_x) * side_constant

    charge_pct = TennisGetFloat("Self Swing Charge Pct")
    should_charge = CompareBool(
        arrival_time < 1,
        charge_pct > 0,
        "or"
    )
    should_hit = CompareBool(
        CompareBool(
            in_range,
            CompareBool(
                racket1_dist <= 1.05,
                racket2_dist <= 1.05,
                "or"
            )
        ),
        x_dist < -1.85,
        "or"
    )

    return CompareBool(should_charge, ~should_hit, "and")
