from AIGamePyLibrary.AIGamePyLibrary import *

def awaiting_hit_move_controller():
    center_half = TennisGetVector3("Center Of Half")
    center_back = TennisGetVector3("Center Of Back")

    b2h_vec = center_half-center_back

    # Possibly implement opponent average scoring location to cover it more
    # Or experiment with Estimated Opponent Shot Location (might need to aim wrong before hitting to confuse opponents)

    return center_back + 0.5 * b2h_vec

def receiving_move_controller():
    predicted_bounce = TennisGetVector3("Predicted Bounce")
    ball_velocity = TennisGetVector3("Ball Velocity")

    return predicted_bounce + ball_velocity # make this calculate the distance where the ball will be back to racket height (will require estimating ball velocity loss)

def awaiting_serve_move_controller():
    opponent_aces = TennisGetFloat("Opponent Aces")
    opponent_points = TennisGetFloat("Opponent Points")

    ace_pct = opponent_aces / opponent_points

    receive_pos = TennisGetVector3("Receive Stance")
    avg_scoring_pos = TennisGetVector3("Opponent Average Scoring Location")

    r2avg_vec = avg_scoring_pos-receive_pos

    # Also here we might want to have a look at Estimated Opponent Shot Location (if not too easily manipulated) 

    return receive_pos + ace_pct * r2avg_vec

def serving_move_controller():
    return TennisGetVector3("Serve Stance")