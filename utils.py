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
    return squash_axes(vector, squash_y=True)

def squash_axes(vector, squash_x=False, squash_y=False, squash_z=False):
    x,y,z = Vector3Split(vector)
    return Vector3(
        0 if squash_x else x,
        0 if squash_y else y,
        0 if squash_z else z
    )

def skew_move_target(move_target, aim_target):
    """
    Skew the move target so racket position once aimed will be at the interception point
    """
    aim_vector = SubtractVector3(aim_target, move_target)

def racket_offset_plotting():
    racket_trans = TennisGetTransform("Self Racket Center")
    racket_pos = RelativePosition(racket_trans, "Self")
    horizontal_racket = squash_y_axis(racket_pos)

    ball_pos = TennisGetVector3("Ball Position")
    horizontal_ball = squash_y_axis(ball_pos)

    horizontal_distance = Distance(horizontal_racket, horizontal_ball)

    y_offset = ConditionalSetFloat(
        horizontal_distance <= 1.05,
        1,
        ConditionalSetFloat(
            horizontal_distance <= 1.85,
            2,
            3
        )
    )

    line = DebugDrawLine(
        racket_pos + Vector3(0,2,0),
        racket_pos + Vector3(0,2+y_offset,0),
        0.5,
        "Blonde"
    )

def max_float(nodes):
    max_value = nodes[0]
    for node in nodes:
        max_value = ConditionalSetFloat(
            node > max_value,
            node,
            max_value
        )
    return max_value

def max_vector3(vectors, float_keys):
    max_vector = vectors[0]
    max_float = float_keys[0]
    for i in range(1, len(vectors)):
        max_vector = ConditionalSetVector3(
            float_keys[i] > max_float,
            vectors[i],
            max_vector
        )
        max_float = ConditionalSetFloat(
            float_keys[i] > max_float,
            float_keys[i],
            max_float
        )
    return max_vector

def min_float(nodes):
    min_value = nodes[0]
    for node in nodes:
        min_value = ConditionalSetFloat(
            node < min_value,
            node,
            min_value
        )
    return min_value

def min_vector3(vectors, float_keys):
    min_vector = vectors[0]
    min_float = float_keys[0]
    for i in range(1, len(vectors)):
        min_vector = ConditionalSetVector3(
            float_keys[i] < min_float,
            vectors[i],
            min_vector
        )
        min_float = ConditionalSetFloat(
            float_keys[i] < min_float,
            float_keys[i],
            min_float
        )
    return min_vector

def plot_trajectory(trajectory, color="Black"):
    for i in range(len(trajectory)-1):
        _ = DebugDrawLine(
            trajectory[i],
            trajectory[i+1],
            0.5,
            color
        )
