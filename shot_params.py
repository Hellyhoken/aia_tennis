import json

import numpy as np

from AIGamePyLibrary.AIGamePyLibrary import *
from params import SHOT_TYPES     

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
        file_path = f"bounce_recordings/{shot_type.lower()}.json"
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
        file_path = f"bounce_recordings/{shot_type.lower()}.json"
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

def get_shot_speed(debug=False):
    shot_speeds = {}
    for shot_type in SHOT_TYPES:
        file_path = f"bounce_recordings/{shot_type.lower()}.json"
        with open(file_path, "r") as f:
            string = f.readlines()
        string = "".join(string)
        for i in range(10):
            string = string.replace(f",{i}",f".{i}")
        data = json.loads(string)
        series = {entry["name"]: entry["y"] for entry in data["series"]}
        horizontal_velocities = np.array([np.linalg.norm([vx, vz]) for vx, vz in zip(series["vx"], series["vz"])])
        mask = horizontal_velocities > 0
        shot_speeds[shot_type] = np.mean(horizontal_velocities[mask])
    if debug:
        print(json.dumps(shot_speeds, indent=4))
    return shot_speeds


if __name__ == "__main__":
    get_bounce_params(debug=True, plot=True)
    get_shot_params(debug=True)
    get_shot_speed(debug=True)
    input("Press Enter to exit...")