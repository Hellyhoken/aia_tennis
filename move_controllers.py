from AIGamePyLibrary.AIGamePyLibrary import *

from utils import squash_y_axis

def awaiting_hit_move_controller():
    center_half = TennisGetVector3("Center Of Half")
    center_back = TennisGetVector3("Center Of Back")

    b2h_vec = center_half-center_back

    # Possibly implement opponent average scoring location to cover it more
    # Or experiment with Estimated Opponent Shot Location (might need to aim wrong before hitting to confuse opponents)

    return center_back + 0.5 * b2h_vec

def receiving_move_controller():
    predicted_bounce = TennisGetVector3("Predicted Bounce")
    ball_velocity = squash_y_axis(TennisGetVector3("Ball Velocity"))

    pre_bounce = predicted_bounce + ball_velocity * 0.05 # make this calculate the distance where the ball will be back to racket height (will require estimating ball velocity loss)

    must_wait = TennisGetBool("Must Wait For Bounce")
    has_bounced = TennisGetBool("Ball Has Bounced")

    ball_position = TennisGetVector3("Ball Position")
    player_transform = TennisGetTransform("Self")
    player_position = RelativePosition(player_transform, "Self")
    b2p_vec = player_position - ball_position

    norm_vel = ball_velocity * (1/Magnitude(ball_velocity))
    target_offset = DotProduct(norm_vel, b2p_vec)
    target_offset = ConditionalSetFloat(target_offset > 0, target_offset, 0)

    post_bounce = high_ball_check(target_offset, norm_vel, ball_position, player_position)

    ball_plot = DebugDrawDisc(post_bounce, 0.5, 0.5, "Hot Pink")

    do_pre_bounce = CompareBool(~has_bounced, must_wait, "and")

    return ConditionalSetVector3(
        do_pre_bounce,
        pre_bounce,
        post_bounce
    )

def awaiting_serve_move_controller():
    receive_pos = TennisGetVector3("Receive Stance")

    return receive_pos

def serving_move_controller():
    return TennisGetVector3("Serve Stance")

def high_ball_check(target_offset, norm_vel, ball_position, player_position):
    has_bounced = TennisGetBool("Ball Has Bounced")

    orig = ball_position + norm_vel * target_offset
    pred_bounce = TennisGetVector3("Predicted Bounce")

    bb_dist = squash_y_axis(ball_position-pred_bounce)
    orig_clamp = ConditionalSetVector3(
        CompareFloats(bb_dist, target_offset, "<"),
        pred_bounce,
        orig
    )

    l11 = GetVariable("height_limit1_start")
    l12 = GetVariable("height_limit1_end")

    if11 = CompareFloats(target_offset, l11, ">")
    if12 = CompareFloats(target_offset, l12, "<")
    if1 = CompareBool(if11, if12)

    t11 = GetVariable("height_limit1_start_time")
    t12 = GetVariable("height_limit1_end_time")

    first = ConditionalSetVector3(
        if1,
        determine_height_limit_pos(
            l11,
            l12,
            t11,
            t12,
            norm_vel,
            ball_position,
            player_position
        ),
        orig_clamp
    )

    l21 = GetVariable("height_limit2_start")
    l22 = GetVariable("height_limit2_end")

    if21 = CompareFloats(target_offset, l21, ">")
    if22 = CompareFloats(target_offset, l22, "<")
    if2 = CompareBool(CompareBool(if21, if22), ~has_bounced)

    t21 = GetVariable("height_limit2_start_time")
    t22 = GetVariable("height_limit2_end_time")

    second = ConditionalSetVector3(
        if2,
        determine_height_limit_pos(
            l21,
            l22,
            t21,
            t22,
            norm_vel,
            ball_position,
            player_position,
            c1="Yellow",
            c2="Black"
        ),
        first
    )

    return second

def determine_height_limit_pos(
    l1,
    l2,
    t1,
    t2,
    norm_vel,
    ball_position,
    player_position,
    c1 = "Dark Green",
    c2 = "Purple"
):
    p1 = ball_position + ScaleVector3(norm_vel, l1)
    p2 = ball_position + ScaleVector3(norm_vel, l2)

    debug_circ1 = DebugDrawDisc(p1, 0.5, 0.5, c1)
    debug_circ2 = DebugDrawDisc(p2, 0.5, 0.5, c2)

    d1 = Magnitude(squash_y_axis(p1-player_position))
    d2 = Magnitude(squash_y_axis(p2-player_position))

    v1 = DivideFloats(d1, t1)
    v2 = DivideFloats(d2, t2)

    take_first = CompareBool(
        CompareFloats(t1, 0, ">"),
        CompareBool(
            CompareFloats(v1, 8, "<="),
            v1 <= v2,
            "or"
        )
    )

    return ConditionalSetVector3(
        take_first,
        p1,
        p2
    )