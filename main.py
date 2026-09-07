import argparse
import os

from AIGamePyLibrary.AIGamePyLibrary import *

from controllers import *
from kast_parabel import kast_parabel
from mode_selector import mode_selector
from utils import (
    squash_axes,
    racket_offset,
    plot_bool,
    racket_offset_plotting
)

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
    racket_offset_plotting()

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
    give_up_var = GetVariable("give_up")

    sprint_bool = CompareBool(sprint_var, Not(give_up_var))

    racket_x_vec = squash_axes(GetVariable("racket_offset"),False,True,True)
    move_target = SubtractVector3(move_var, racket_x_vec*0.6)

    # Controller
    auto_move = TennisAutoMove(move_target, aim_var)
    controller = TennisController(auto_move, swing_var, shot_var, sprint_bool)

    i = 0
    while True:
        save_path = f"bots/hh_botv{args.version_number}.{i}.txt"
        if os.path.isfile(save_path):
            i += 1
            continue
        else:
            SaveData(save_path, "auto")
            break