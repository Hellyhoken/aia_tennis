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

def move_controller():
    awaiting_hit_move = ConditionalSetVector3(
        GetVariable("awaiting_hit"),
        awaiting_hit_move_controller(),
        TennisGetVector3("Center Of Half")
    )

    receiving_move = ConditionalSetVector3(
        GetVariable("receiving"),
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
        False
    )
    receiving_swing = ConditionalSetBool(
        GetVariable("receiving"),
        receiving_swing_controller(),
        serving_swing
    )
    return SetVariable("swing", receiving_swing)

def shot_controller():
    shot = TennisGetFloat("Shot: Flat")
    shot = ConditionalSetFloat(GetVariable("hitting_corner") == 2,TennisGetFloat("Shot: Curve Right"),shot)
    shot = ConditionalSetFloat(GetVariable("hitting_corner") == 3,TennisGetFloat("Shot: Curve Left"),shot)

    return SetVariable("shot", shot)

def sprint_controller():
    sprint_bool = False
    return SetVariable("sprint", sprint_bool)