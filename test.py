from AIGamePyLibrary.AIGamePyLibrary import *

from trajectory_predicter import step_score_function

_ = step_score_function()

player_pos = RelativePosition(TennisGetTransform("Self"), "Self")
ball_pos = TennisGetVector3("Ball Position")
ball_incoming = TennisGetBool("Ball Incoming")

_ = Debug(CustomFunction("trajectory_predicter_step_score", player_pos, ball_pos, 0.04, ball_incoming))

SaveData("bots/test.txt", "auto")