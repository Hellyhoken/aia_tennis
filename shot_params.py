import json

import numpy as np

from AIGamePyLibrary.AIGamePyLibrary import *
from targets import SIDE_FLOAT

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

def get_pre_bounce_trajectories(series):
    pre_bounce_trajs = []
    vy = series["vy"]
    vx = series["vx"]
    vz = series["vz"]
    i = 0
    while i < len(vy)-1:
        if ((vx[i] == 0 and vy[i] == 0 and vz[i] == 0) and 
            not (vx[i+1] == 0 and vy[i+1] == 0 and vz[i+1] == 0)):
            i += 1
            pre_bounce_traj = []
            while i < len(vy)-1 and vy[i] > vy[i+1]:
                pre_bounce_traj.append((vx[i], vy[i], vz[i]))
                i += 1
            pre_bounce_trajs.append(pre_bounce_traj)
        i += 1
    return pre_bounce_trajs

def extract_pre_post(vy,v1,v2=[]):
    pre_vy = []
    post_vy = []
    pre_v1 = []
    post_v1 = []
    pre_v2 = []
    post_v2 = []
    for i in range(len(vy)-1):
        if vy[i] < 0 and vy[i+1] > 0:
            pre_vy.append(vy[i])
            post_vy.append(vy[i+1])
            pre_v1.append(v1[i])
            post_v1.append(v1[i+1])
            if v2:
                pre_v2.append(v2[i])
                post_v2.append(v2[i+1])

    if not v2:
        return pre_vy, post_vy, pre_v1, post_v1
    else: return (pre_vy, post_vy), (pre_v1, post_v1), (pre_v2, post_v2)

def least_squares(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum([x[i]*y[i] for i in range(n)])
    sum_x2 = sum([x[i]**2 for i in range(n)])

    slope = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x**2)
    intercept = (sum_y - slope*sum_x) / n

    return slope, intercept

def get_bounce_params(debug=False, plot=False):
    bounce_params = {}
    for shot_type in SHOT_TYPES:
        file_path = f"bounce_recordings/{shot_type}.json"
        with open(file_path, "r") as f:
            string = f.readlines()
        string = "".join(string)
        for i in range(10):
            string = string.replace(f",{i}",f".{i}")
        data = json.loads(string)
        series = {entry["name"]: entry["y"] for entry in data["series"]}
        vy_pairs, vx_pairs, vz_pairs = extract_pre_post(series["vy"], series["vx"], series["vz"])

        vy_k, vy_m = least_squares(*vy_pairs)
        vx_k, vx_m = least_squares(*vx_pairs)
        vz_k, vz_m = least_squares(*vz_pairs)

        bounce_params[shot_type] = {
            "vy": {"k": vy_k, "m": vy_m},
            "vx": {"k": vx_k, "m": vx_m},
            "vz": {"k": vz_k, "m": vz_m}
        }
        if plot:
            import matplotlib.pyplot as plt
            fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
            ax1.scatter(*vy_pairs, label="vy")
            x = [x for x in vy_pairs[0]]
            y = [vy_k * x_i + vy_m for x_i in x]
            ax1.plot(x, y, color="red")
            ax2.scatter(*vx_pairs, label="vx")
            x = [x for x in vx_pairs[0]]
            y = [vx_k * x_i + vx_m for x_i in x]
            ax2.plot(x, y, color="red")
            ax3.scatter(*vz_pairs, label="vz")
            x = [x for x in vz_pairs[0]]
            y = [vz_k * x_i + vz_m for x_i in x]
            ax3.plot(x, y, color="red")
            ax1.legend()
            ax2.legend()
            ax3.legend()
            fig.suptitle(f"{shot_type} bounce params")
            plt.show(block=False)

    if debug:
        print(json.dumps(bounce_params, indent=4))

def get_shot_params(debug=False):
    shot_params = {}
    for shot_type in SHOT_TYPES:
        file_path = f"bounce_recordings/{shot_type}.json"
        with open(file_path, "r") as f:
            string = f.readlines()
        string = "".join(string)
        for i in range(10):
            string = string.replace(f",{i}",f".{i}")
        data = json.loads(string)
        series = {entry["name"]: entry["y"] for entry in data["series"]}
        pre_bounce_trajs = get_pre_bounce_trajectories(series)

        accelerations = np.mean([np.mean(np.diff(traj, axis=0)/0.019, axis=0) for traj in pre_bounce_trajs if traj], axis=0)
        shot_params[shot_type] = {
            "ax": accelerations[0],
            "ay": accelerations[1],
            "az": accelerations[2]
        }
        if debug:
            stdevs = np.mean([np.std(np.diff(traj, axis=0)/0.019, axis=0) for traj in pre_bounce_trajs if traj], axis=0)
            if np.any(stdevs > 0.1):
                print(f"Warning: High standard deviation in {shot_type} pre-bounce accelerations: {stdevs}")
    if debug:
        print(json.dumps(shot_params, indent=4))
    return shot_params

if __name__ == "__main__":
    get_bounce_params(debug=True, plot=True)
    get_shot_params(debug=True)
    input("Press Enter to exit...")