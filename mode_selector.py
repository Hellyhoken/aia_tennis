from AIGamePyLibrary.AIGamePyLibrary import *

def mode_selector():
    serve_phase = TennisGetBool("Is Serve Phase")
    play_phase = Not(serve_phase)

    self_server = TennisGetBool("Is Self Server For Set")
    opponent_server = TennisGetBool("Is Opponent Server For Set")

    self_serving = And(serve_phase, self_server)
    opponent_serving = And(serve_phase, opponent_server)

    wait_bounce = TennisGetBool("Must Wait For Bounce")
    incomming_ball = TennisGetBool("Ball Incoming")

    receiving_serve = And(And(play_phase, incomming_ball), wait_bounce)
    receiving = And(And(play_phase, incomming_ball), Not(wait_bounce))
    awaiting_hit = And(play_phase, Not(incomming_ball))

    return [
        SetVariable("serving", self_serving),
        SetVariable("awaiting_opponent_serve", opponent_serving),
        SetVariable("receiving_serve", receiving_serve),
        SetVariable("recieving", receiving), # possibly divide into lob, flat or charged
        SetVariable("awaiting_opponet_hit", awaiting_hit) # possibly divide into charged (cannot be returned as charged?) or not charged
    ]