from AIGamePyLibrary.AIGamePyLibrary import *
from params import SIDE_FLOAT, shot_params_getter
from mode_selector import BALL_INCOMING
import params
from utils import max_float, max_vector3, plot_trajectory, squash_y_axis

OUT_POS = Vector3(0, 0, 100)

SCORE_NO_REACH = -10000
SCORE_TIME = 1
SCORE_WALK = ConditionalSetFloat(BALL_INCOMING, 100, 0)
SCORE_VELOCITY = ConditionalSetFloat(BALL_INCOMING, 1, 0)
SCORE_HEIGHT = ConditionalSetFloat(BALL_INCOMING, 1, 0)

def bounced_velocity(velocity, shot_params):
    vx, vy, vz = Vector3Split(velocity)
    vy_k = shot_params["vy_k"]
    vy_m = shot_params["vy_m"]
    vx_k = shot_params["vx_k"]
    vz_k = shot_params["vz_k"]
    vz_m = shot_params["vz_m"]

    new_vx = vx * vx_k
    new_vy = vy * vy_k + vy_m
    new_vz = vz * vz_k + vz_m

    return Vector3(new_vx, new_vy, new_vz)

def get_ball_trajectory():
    side_float = ConditionalSetFloat(
        BALL_INCOMING,
        SIDE_FLOAT,
        -SIDE_FLOAT
    )

    ball_pos = TennisGetVector3("Ball Position")
    ball_vel = TennisGetVector3("Ball Velocity")

    ball_bounced = TennisGetBool("Ball Has Bounced")
    shot_type = ConditionalSetFloat(
        ball_bounced,
        TennisGetFloat("Shot: Flat"),
        TennisGetFloat("Shot: Ball")
    )

    shot_params = shot_params_getter(~BALL_INCOMING, shot_type)
    ball_acc = Vector3(shot_params["ax"], shot_params["ay"], shot_params["az"])

    time_step = 0.04
    time = 0.0

    player_pos = ConditionalSetVector3(
        BALL_INCOMING,
        RelativePosition(TennisGetTransform("Self"), "Self"),
        RelativePosition(TennisGetTransform("Opponent"), "Self")
    )

    _ = step_score_function()

    positions = [ball_pos]
    times = [time]
    scores = [
        ConditionalSetFloat(
            Distance(player_pos, ball_pos) < 3.0,
            -SCORE_NO_REACH,
            SCORE_NO_REACH
        )
    ]
    bounced_acc = Vector3(0, -28, 0)
    for _ in range(50):
        # Trajectory prediction
        new_ball_pos = AddVector3(ball_pos, ScaleVector3(ball_vel, time_step))
        new_ball_vel = AddVector3(ball_vel, ScaleVector3(ball_acc, time_step))

        # Bounce handling
        _, ball_y, _ = Vector3Split(new_ball_pos)
        bounced = ball_y <= 0.0
        bounce_time = (Distance(ball_pos, TennisGetVector3("Predicted Bounce")) / Magnitude(ball_vel))
        time_left = time_step - bounce_time
        pre_bounce_vel = AddVector3(ball_vel, ScaleVector3(ball_acc, bounce_time))
        bounced_vel = ConditionalSetVector3(
            ball_bounced,
            Vector3(0, 0, 0),
            AddVector3(bounced_velocity(pre_bounce_vel, shot_params), ScaleVector3(bounced_acc, time_left))
        )
        bounced_pos = ConditionalSetVector3(
            ball_bounced,
            OUT_POS,
            TennisGetVector3("Predicted Bounce") + ScaleVector3(bounced_vel, time_left)
        )
        new_ball_acc = ConditionalSetVector3(
            ball_bounced,
            Vector3(0, 0, 0),
            bounced_acc
        )

        ball_pos = ConditionalSetVector3(
            bounced,
            bounced_pos,
            new_ball_pos
        )
        ball_vel = ConditionalSetVector3(
            bounced,
            bounced_vel,
            new_ball_vel
        )
        ball_acc = ConditionalSetVector3(
            bounced,
            new_ball_acc,
            ball_acc
        )
        ball_bounced = ConditionalSetBool(
            bounced,
            True,
            ball_bounced
        )

        time = time + time_step
        positions.append(ball_pos)
        times.append(time)
        # Score of interception
        
        scores.append(CustomFunction(
            "trajectory_predicter_step_score",
            player_pos,
            ball_pos,
            time,
            ball_bounced
        ))

    return positions, times, scores

def step_score_function():
    fn = CreateFunction("trajectory_predicter_step_score")
    player_pos, ball_pos, time, ball_bounced = fn.Param1, fn.Param2, fn.Param3, fn.Param4
    mo = AssignToFunction(Float(-4.0), fn)
    zero = AssignToFunction(Float(0.0), fn)
    zf = AssignToFunction(Float(0.3), fn)
    two = AssignToFunction(Float(2.0), fn)
    four = AssignToFunction(Float(4.0), fn)
    ept = AssignToFunction(Float(8.3), fn)
    tt = AssignToFunction(Float(13.0), fn)
    oh = AssignToFunction(Float(100.0), fn)
    mtt = AssignToFunction(Float(-10000.0), fn)
    ball_x, ball_y, _ = Vector3Split(ball_pos)
    ball_x = AssignToFunction(ball_x, fn)
    ball_y = AssignToFunction(ball_y, fn)
    player_x, _, _ = Vector3Split(player_pos)
    player_x = AssignToFunction(player_x, fn)
    b2p = AssignToFunction(SubtractVector3(ball_pos, player_pos), fn)
    b2p_x, _, b2p_z = Vector3Split(b2p)
    b2p_x = AssignToFunction(b2p_x, fn)
    b2p_z = AssignToFunction(b2p_z, fn)
    b2p_flat = AssignToFunction(Vector3(b2p_x, zero, b2p_z), fn)
    distance = AssignToFunction(Magnitude(b2p_flat), fn)
    required_velocity = AssignToFunction(DivideFloats(distance, time), fn)
    reachable_height = AssignToFunction(ball_y <= four, fn)
    height_score = AssignToFunction(MultiplyFloats(ball_y, zf), fn)
    height_score = AssignToFunction(ConditionalSetFloat(
        reachable_height,
        height_score,
        zero
    ), fn)
    time_score = AssignToFunction(MultiplyFloats(mo, time), fn)
    walk_condition = AssignToFunction(required_velocity <= ept, fn)
    walk_score = AssignToFunction(ConditionalSetFloat(
        walk_condition,
        oh,
        zero
    ), fn)
    vel_diff = AssignToFunction(ept - required_velocity, fn)
    velocity_score = AssignToFunction(vel_diff, fn)
    clamp_vel = AssignToFunction(velocity_score > zero, fn)
    velocity_score = AssignToFunction(ConditionalSetFloat(
        clamp_vel,
        velocity_score,
        zero
    ), fn)
    not_reachable_velocity = AssignToFunction(required_velocity > tt, fn)
    not_reachable_height = AssignToFunction(Not(reachable_height), fn)
    x_diff = AssignToFunction(ball_x - player_x, fn)
    x_dist = AssignToFunction(Abs(x_diff), fn)
    x_abs = AssignToFunction(Abs(player_x), fn)
    not_reachable_side = AssignToFunction(x_dist > x_abs, fn)
    not_reachable = AssignToFunction(CompareBool(not_reachable_velocity, not_reachable_height, "or"), fn)
    not_reachable = AssignToFunction(CompareBool(not_reachable, not_reachable_side, "or"), fn)
    no_reach_score = AssignToFunction(ConditionalSetFloat(
        not_reachable,
        mtt,
        zero
    ), fn)
    must_wait = AssignToFunction(TennisGetBool("Must Wait For Bounce"), fn)
    nbb = AssignToFunction(Not(ball_bounced), fn)
    pred_bounce = AssignToFunction(TennisGetVector3("Predicted Bounce"), fn)
    dist_to_bounce = AssignToFunction(Distance(ball_pos, pred_bounce), fn)
    too_close_to_bounce = AssignToFunction(dist_to_bounce < two, fn)
    foul = AssignToFunction(CompareBool(too_close_to_bounce, nbb, "or"), fn)
    foul = AssignToFunction(CompareBool(foul, must_wait), fn)
    foul_score = AssignToFunction(ConditionalSetFloat(
        foul,
        mtt,
        zero
    ), fn)
    score = AssignToFunction(height_score + time_score, fn)
    score = AssignToFunction(score + walk_score, fn)
    score = AssignToFunction(score + velocity_score, fn)
    score = AssignToFunction(score + no_reach_score, fn)
    score = AssignToFunction(score + foul_score, fn)

    return SetFunctionReturn(fn, score)

def trajectory_predicter():
    ball_trajectory, times, scores = get_ball_trajectory()
    intercept_point = max_vector3(ball_trajectory, scores)
    intercept_time = max_float(times, scores)
    plot_trajectory(ball_trajectory)
    _ = DebugDrawDisc(intercept_point, 0.5, 0.5, "Red")
    return intercept_point, intercept_time

INTERCEPT_POINT, INTERCEPT_TIME = trajectory_predicter()