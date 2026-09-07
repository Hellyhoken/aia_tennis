import argparse
import os

from AIGamePyLibrary.AIGamePyLibrary import *

from controllers import *
from kast_parabel import kast_parabel
from mode_selector import mode_selector
from utils import racket_offset, plot_bool

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

    # Util variables
    r_offset = racket_offset()
    kast_parabel()

    # Mode selection
    modes = mode_selector()

    # Controls
    moving = move_controller()
    aiming = aim_controller()
    swining = swing_controller()
    shooting = shot_controller()
    sprinting = sprint_controller()

    # Control variables
    move_var = GetVariable("move")
    aim_var = GetVariable("aim")
    swing_var = GetVariable("swing")
    shot_var = GetVariable("shot")
    sprint_var = GetVariable("sprint")

    move_target = SubtractVector3(move_var, GetVariable("racket_offset"))

    # Controller
    auto_move = TennisAutoMove(move_var, aim_var)
    controller = TennisController(auto_move, swing_var, shot_var, sprint_var)

    i = 0
    while True:
        save_path = f"bots/hh_botv{args.version_number}.{i}.txt"
        if os.path.isfile(save_path):
            i += 1
            continue
        else:
            SaveData(save_path, "auto")
            break