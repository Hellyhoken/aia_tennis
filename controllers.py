from AIGamePyLibrary.AIGamePyLibrary import *

from move_controllers import (
    awaiting_hit_move_controller,
    receiving_move_controller,
    awaiting_serve_move_controller,
    serving_move_controller
)
from swing_controllers import (
    serving_swing_controller,
    receiving_swing_controller
)
from aim_controllers import (
    old_aim_controller,
    aim_away_controller
)
from sprint_controllers import (
    sprint_info
)
def move_controller():
    awaiting_hit_move = ConditionalSetVector3(
        GetVariable("awaiting_hit"),
        awaiting_hit_move_controller(),
        TennisGetVector3("Center Of Half")
    )

    receiving_move = ConditionalSetVector3(
        CompareBool(GetVariable("receiving"), Not(GetVariable("ball_out"))),
        receiving_move_controller(),
        awaiting_hit_move
    )

    awaiting_serve_move = ConditionalSetVector3(
        GetVariable("awaiting_serve"),
        awaiting_serve_move_controller(),
        receiving_move
    )

    serving_move = ConditionalSetVector3(
        GetVariable("serving"),
        serving_move_controller(),
        awaiting_serve_move
    )

    return SetVariable("move", serving_move)

def aim_controller():
    aim_target=ConditionalSetVector3(GetVariable("serving"),old_aim_controller(),aim_away_controller())
     
  
    SetVariable("aim",aim_target )

def swing_controller():
    serving_swing = ConditionalSetBool(
        GetVariable("serving"),
        serving_swing_controller(),
        receiving_swing_controller()
    )
    return SetVariable("swing", serving_swing)

def shot_controller():
    shot = TennisGetFloat("Shot: Flat")
    shot = ConditionalSetFloat(GetVariable("hitting_corner") == 2,TennisGetFloat("Shot: Curve Right"),shot)
    shot = ConditionalSetFloat(GetVariable("hitting_corner") == 3,TennisGetFloat("Shot: Curve Left"),shot)
    

    return SetVariable("shot", shot)

def sprint_controller():
    should_sprint,give_up = sprint_info()

    ball_incoming = TennisGetBool("Ball Incoming")
    has_bounced = TennisGetBool("Ball Has Bounced")
    predicted_bounce = TennisGetVector3("Predicted Bounce")
    pred_x, _, pred_z = Vector3Split(predicted_bounce)

    ball_out = CompareBool(ball_incoming, CompareBool(~has_bounced, CompareBool(Abs(pred_z) > 6, Abs(pred_x) > 14, "or")))

    SetVariable("ball_out", ball_out)
    SetVariable("give_up",CompareBool(give_up, ball_out, "or"))
    return SetVariable("sprint", should_sprint)