import numpy as np

from AIGamePyLibrary.AIGamePyLibrary import *
from utils import squash_axes

aim_x_coords = np.linspace(1.0, 13.9, 4)
aim_z_coords = np.linspace(-5.9, 5.9, 2)
move_x_coords = np.linspace(2.61, 14.0, 13)
move_z_coords = np.linspace(-6.0, 6.0, 13)


aim_targets = np.array([[x, z] for x in aim_x_coords for z in aim_z_coords])
move_targets = np.array([[x, z] for x in move_x_coords for z in move_z_coords])
drop_targets = np.array([[0.1, z] for z in aim_z_coords])

SIDE_FLOAT = ConditionalSetFloat(
    TennisGetBool("Is Home"), 1.0, -1.0
)

OPPONENT_TARGETS = [
    Vector3(x * -SIDE_FLOAT, 0, z) for x, z in aim_targets
]

OPPONENT_DROP_TARGETS = [
    Vector3(x * -SIDE_FLOAT, 0, z) for x, z in drop_targets
]

OPPONENT_LOB_TARGET = Vector3(13.9 * -SIDE_FLOAT, 0, 0) + squash_axes(RelativePosition(TennisGetTransform("Opponent"), "Self"), squash_x=True, squash_y=True)

SELF_TARGETS = [
    Vector3(x * SIDE_FLOAT, 0, z) for x, z in aim_targets
]

SELF_DROP_TARGETS = [
    Vector3(x * SIDE_FLOAT, 0, z) for x, z in drop_targets
]

SELF_LOB_TARGET = Vector3(13.9 * SIDE_FLOAT, 0, 0) + squash_axes(RelativePosition(TennisGetTransform("Self"), "Self"), squash_x=True, squash_y=True)

MOVE_TARGETS = [
    Vector3(x * -SIDE_FLOAT, 0, z) for x, z in move_targets
]
