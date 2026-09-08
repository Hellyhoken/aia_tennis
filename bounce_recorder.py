from AIGamePyLibrary.AIGamePyLibrary import *

ball_vel = TennisGetVector3("Ball Velocity")

vx, vy, vz = Vector3Split(ball_vel)

_ = TimePlot("vx", "Auburn", "", vx)
_ = TimePlot("vy", "Auburn", "", vy)
_ = TimePlot("vz", "Auburn", "", vz)

SaveData("bots/bounce_recorder.txt", "auto")