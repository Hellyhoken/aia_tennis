import numpy as np

from AIGamePyLibrary.AIGamePyLibrary import *
from utils import squash_axes

AIM_X_COORDS = np.linspace(2.0, 14.0, 48)
move_x_coords = np.linspace(2.61, 8, 6)
move_z_coords = np.linspace(-6.0, 6.0, 9)

move_targets = np.array([[x, z] for x in move_x_coords for z in move_z_coords])

SIDE_FLOAT = ConditionalSetFloat(
    TennisGetBool("Is Home"), 1.0, -1.0
)

SERVE_SIDE_FLOAT = ConditionalSetFloat(
    TennisGetBool("Is Ad Court Serve"), -1.0, 1.0
)

SERVE_OFFSET = Vector3(0.5, 0, 3.0)

INCOMING_FLOAT = ConditionalSetFloat(
    TennisGetBool("Ball Incoming"), 1.0, -1.0
)

TARGETS = [Vector3(x * SIDE_FLOAT, 0, 6) for x in AIM_X_COORDS]

MOVE_TARGETS = [
    Vector3(x * -SIDE_FLOAT, 0, z) for x, z in move_targets
]

SHOT_TYPES = [
    "Flat",
    "Slice",
    "Topspin",
    "Lob",
    "Drop",
    "Right",
    "Left"
]

CURVES = {
    "Right",
    "Left"
}

NEED_SIDE_FLOAT = {
    "Right",
    "Left",
    "Slice",
    "Lob",
    "Drop"
}

SHOT_PARAMS = {
    "Flat": {"vy_k": -0.78, "vy_m": 0.33, "vx_k": 0.94, "vz_k": 0.94, "vz_m": 0.0, "ax": 0.0, "ay": -28.0, "az": 0.0},
    "Slice": {"vy_k": -0.63, "vy_m": 0.34, "vx_k": 0.9, "vz_k": 0.9, "vz_m": 0.0, "ax": -1.0, "ay": -28.0, "az": 0.0},
    "Topspin": {"vy_k": -1.10, "vy_m": 0.6, "vx_k": 1.13, "vz_k": 1.13, "vz_m": 0.0, "ax": 0.0, "ay": -28.0, "az": 0.0},
    "Lob": {"vy_k": -0.78, "vy_m": 0.33, "vx_k": 0.94, "vz_k": 0.94, "vz_m": 0.0, "ax": -0.45, "ay": -28.0, "az": 0.0},
    "Drop": {"vy_k": -0.34, "vy_m": 6.16, "vx_k": 0.4, "vz_k": 0.4, "vz_m": 0.0, "ax": -0.45, "ay": -28.0, "az": 0.0},
    "Right": {"vy_k": -0.78, "vy_m": 0.25, "vx_k": 0.94, "vz_k": 0.94, "vz_m": -0.18, "ax": 0.0, "ay": -28.0, "az": -16.0},
    "Left": {"vy_k": -0.78, "vy_m": 0.25, "vx_k": 0.94, "vz_k": 0.94, "vz_m": 0.18, "ax": 0.0, "ay": -28.0, "az": 16.0}
}

SHOT_SPEEDS = {
    "Flat": 20,
    "Slice": 30,
    "Topspin": 20,
    "Lob": 10,
    "Drop": 16,
    "Right": 27,
    "Left": 27
}

def apply_side_float(params, side_float):
    params["vz_m"] = params["vz_m"] * side_float
    params["ax"] = params["ax"] * side_float
    params["az"] = params["az"] * side_float

    return params

def shot_params_getter(is_self, shot_type):
    side_float = ConditionalSetFloat(
        is_self,
        SIDE_FLOAT,
        -SIDE_FLOAT
    )
    shot_params = SHOT_PARAMS["Flat"]
    for shot in SHOT_TYPES:
        ts_params = apply_side_float(SHOT_PARAMS[shot], side_float) if shot in NEED_SIDE_FLOAT else SHOT_PARAMS[shot]
        is_shot = shot_type == TennisGetFloat(f"Shot: Curve {shot}" if shot in CURVES else f"Shot: {shot}")
        for param in ts_params:
            shot_params[param] = ConditionalSetFloat(
                is_shot,
                ts_params[param],
                shot_params[param]
            )

    return shot_params  
