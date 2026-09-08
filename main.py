import argparse
import os

from AIGamePyLibrary.AIGamePyLibrary import *

from controllers import *
from params import SIDE_FLOAT
from utils import plot_bool

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version-number",
        default=0,
        type=int,
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    # Properties
    properties = ConstructTennisProperties(
        name="Hellyhoken",
        country="Sweden",
        skin="Hot Pink",
        hair_style=3,
        hair_color="Green",
        facial_hair=0
    )

    # Controls
    moving = move_controller()
    aiming = aim_controller()
    swining = swing_controller()
    shooting = shot_controller()
    sprinting, give_up = sprint_controller()

    sprint_bool = CompareBool(sprinting, Not(give_up))

    racket_x_vec = Vector3(0.55, 0, 0) * SIDE_FLOAT
    move_target = SubtractVector3(moving, racket_x_vec*0.6)

    _ = plot_bool(swining, "Swinging", "Yellow")

    # Controller
    auto_move = TennisAutoMove(move_target, aiming)
    controller = TennisController(auto_move, swining, shooting, sprint_bool)

    i = 0
    while True:
        save_path = f"bots/hh_botv{args.version_number}.{i}.txt"
        if os.path.isfile(save_path):
            i += 1
            continue
        else:
            SaveData(save_path, "single")
            break