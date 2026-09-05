from AIGamePyLibrary.AIGamePyLibrary import *

def move_controller():
    move_vector = Vector3(0,0,0)
    return SetVariable("move", move_vector)

def aim_controller():
    move_vector = Vector3(0,0,0)
    return SetVariable("move", move_vector)

def swing_controller():
    swing_bool = True
    return SetVariable("swing", swing_bool)

def shot_controller():
    shot_float = 0
    return SetVariable("shot", shot_float)

def sprint_controller():
    sprint_bool = False
    return SetVariable("sprint", sprint_bool)