from AIGamePyLibrary.AIGamePyLibrary import *

from score_targets import SHOT_TYPE
from trajectory_predicter import INTERCEPT_TIME
from utils import plot_bool, squash_y_axis


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

    ball_position = TennisGetVector3("Ball Position")
    ball_velocity = TennisGetVector3("Ball Velocity")
    
    player_trans = TennisGetTransform("Self")
    player_pos = RelativePosition(player_trans, "Self")

    next_step_ball_pos = ball_position + ball_velocity * 0.065 # 0.019 timestep (0.065 to account for swing delay)

    next_player_distance = Distance(player_pos, next_step_ball_pos)
    in_range = next_player_distance < 3

    racket_x_offset = 0.55 * side_constant

    racket1 = player_pos + Vector3(racket_x_offset, 0, 0.45)
    racket2 = player_pos + Vector3(racket_x_offset, 0, -0.45)

    racket1_dist = Magnitude(squash_y_axis(racket1-next_step_ball_pos))
    racket2_dist = Magnitude(squash_y_axis(racket2-next_step_ball_pos))

    player_x, _, _ = Vector3Split(player_pos)
    racket_x = player_x + racket_x_offset
    next_ball_x, _, _ = Vector3Split(next_step_ball_pos)

    x_dist = (racket_x - next_ball_x) * side_constant

    auto_swing, _ = TennisAutoSwing(SHOT_TYPE, "Prefer Charge")
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

    plot_bool(auto_swing, "Auto Swing", "Red")

    plot_bool(in_range, "In Range", "Green")
    plot_bool(racket1_dist <= 1.05, "Racket 1 In Range", "Blue")
    plot_bool(racket2_dist <= 1.05, "Racket 2 In Range", "Blue")
    plot_bool(x_dist < -1.85, "X Dist < -1.85", "Purple")
    plot_bool(should_hit, "Should Hit", "Blue")

    return CompareBool(auto_swing, ~should_hit, "and")
