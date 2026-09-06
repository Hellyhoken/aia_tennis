from AIGamePyLibrary.AIGamePyLibrary import *

def racket_offset():
    player_transform = TennisGetTransform("Self")
    racket_transform = TennisGetTransform("Self Racket Center")

    player_position = RelativePosition(player_transform, "Self")
    racket_position = RelativePosition(racket_transform, "Self")

    offset = racket_position - player_position

    return SetVariable("racket_offset", offset)

def plot_bool(value, name, color="Black"):
    plot_value = ConditionalSetFloat(
        value,
        1, 0
    )
    return TimePlot(name, color, "", plot_value)

def squash_y_axis(vector):
    x,_,z = Vector3Split(vector)
    return Vector3(x,0,z)

def skew_move_target(move_target, aim_target):
    """
    Skew the move target so racket position once aimed will be at the interception point
    """
    aim_vector = SubtractVector3(aim_target, move_target)


