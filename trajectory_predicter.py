from AIGamePyLibrary.AIGamePyLibrary import *
from shot_params import shot_params_getter
from targets import SIDE_FLOAT
from utils import squash_y_axis

OUT_POS = Vector3(-100, 0, 0)

BALL_INCOMING = TennisGetBool("Ball Incoming")

SCORE_HEIGHT = ConditionalSetFloat(
    BALL_INCOMING,
    10.0,
    0
) 
SCORE_TIME = 1.0
SCORE_WALK = ConditionalSetFloat(
    BALL_INCOMING,
    100.0,
    0
)
SCORE_VELOCITY = ConditionalSetFloat(
    BALL_INCOMING,
    10.0,
    0
)
SCORE_NO_REACH = -10000

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

    positions = [ball_pos]
    scores = [
        ConditionalSetFloat(
            Distance(player_pos, ball_pos) < 3.0,
            -SCORE_NO_REACH,
            SCORE_NO_REACH
        )
    ]
    bounced_acc = Vector3(0, -28, 0)
    for _ in range(100):
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

        # Score of interception
        distance = Magnitude(squash_y_axis(SubtractVector3(player_pos, ball_pos)))
        required_velocity = distance / time
        height_score = ConditionalSetFloat(
            ball_y <= 5.0,
            SCORE_HEIGHT * ball_y,
            0
        )
        time_score = -time * SCORE_TIME
        walk_score = ConditionalSetFloat(
            required_velocity <= 8.3,
            SCORE_WALK,
            0
        )
        velocity_score = SCORE_VELOCITY * (8.3 - required_velocity)
        velocity_score = ConditionalSetFloat(
            velocity_score > 0,
            velocity_score,
            0
        )
        no_reach_score = ConditionalSetFloat(
            CompareBool(required_velocity > 13.0, ball_y > 5.0, "or"),
            SCORE_NO_REACH,
            0
        )
        score = height_score + time_score + walk_score + velocity_score + no_reach_score
        scores.append(score)

    return positions, scores