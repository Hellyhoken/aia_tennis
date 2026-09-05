from AIGamePyLibrary.AIGamePyLibrary import *

from controllers import *
from mode_selector import mode_selector

# Properties
properties = ConstructTennisProperties(
    name="Hellyhoken",
    country="Sweden",
    skin="Hot Pink",
    hair_style=3,
    hair_color="Green",
    facial_hair=0
)

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

# Controller
auto_move = TennisAutoMove(move_var, aim_var)
controller = TennisController(auto_move, swing_var, shot_var, sprint_var)

SaveData("hellyhoken_tennis_bot.txt", "auto")