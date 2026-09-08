from AIGamePyLibrary.AIGamePyLibrary import *

SERVE_PHASE = TennisGetBool("Is Serve Phase")
PLAY_PHASE = ~SERVE_PHASE

SELF_SERVER = TennisGetBool("Is Self Server For Set")
OPPONENT_SERVER = TennisGetBool("Is Opponent Server For Set")

SERVING = CompareBool(SERVE_PHASE, SELF_SERVER, "and")
AWAITING_SERVE = CompareBool(SERVE_PHASE, OPPONENT_SERVER, "and")

BALL_INCOMING = TennisGetBool("Ball Incoming")

RECEIVING = CompareBool(PLAY_PHASE, BALL_INCOMING, "and")
AWAITING_HIT = CompareBool(PLAY_PHASE, ~BALL_INCOMING, "and")

HAS_BOUNCED = TennisGetBool("Ball Has Bounced")
PREDICTED_BOUNCE = TennisGetVector3("Predicted Bounce")

def ball_out():
    pred_x, _, pred_z = Vector3Split(PREDICTED_BOUNCE)
    return CompareBool(BALL_INCOMING, CompareBool(~HAS_BOUNCED, CompareBool(Abs(pred_z) > 6.1, Abs(pred_x) > 14.1, "or")))

BALL_OUT = ball_out()