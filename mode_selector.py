from AIGamePyLibrary.AIGamePyLibrary import *

def mode_selector():
    serve_phase = TennisGetBool("Is Serve Phase")
    play_phase = ~serve_phase

    self_server = TennisGetBool("Is Self Server For Set")
    opponent_server = TennisGetBool("Is Opponent Server For Set")

    self_serving = CompareBool(serve_phase, self_server, "and")
    opponent_serving = CompareBool(serve_phase, opponent_server, "and")

    wait_bounce = TennisGetBool("Must Wait For Bounce")
    incomming_ball = TennisGetBool("Ball Incoming")

    receiving_serve = CompareBool(CompareBool(play_phase, incomming_ball, "and"), wait_bounce, "and")
    receiving = CompareBool(CompareBool(play_phase, incomming_ball, "and"), ~wait_bounce, "and")
    awaiting_hit = CompareBool(play_phase, ~incomming_ball, "and")

    return [
        SetVariable("serving", self_serving),
        SetVariable("awaiting_serve", opponent_serving),
        SetVariable("receiving_serve", receiving_serve),
        SetVariable("recieving", receiving), # possibly divide into lob, flat or charged
        SetVariable("awaiting_hit", awaiting_hit) # possibly divide into charged (cannot be returned as charged?) or not charged
    ]