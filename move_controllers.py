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

    pre_bounce = predicted_bounce + ball_velocity * 0.2 # make this calculate the distance where the ball will be back to racket height (will require estimating ball velocity loss)

    must_wait = TennisGetBool("Must Wait For Bounce")
    has_bounced = TennisGetBool("Ball Has Bounced")

    ball_position = TennisGetVector3("Ball Position")
    player_transform = TennisGetTransform("Self")
    player_position = RelativePosition(player_transform, "Self")
    b2p_vec = player_position - ball_position

    norm_vel = ball_velocity * (1/Magnitude(ball_velocity))
    target_offset = DotProduct(norm_vel, b2p_vec)

    post_bounce = ball_position + norm_vel * target_offset

    do_pre_bounce = CompareBool(~has_bounced, must_wait, "and")

    return ConditionalSetVector3(
        do_pre_bounce,
        pre_bounce,
        post_bounce
    )

def awaiting_serve_move_controller():
    #opponent_aces = TennisGetFloat("Opponent Aces")
    #opponent_points = TennisGetFloat("Opponent Points")

    #ace_pct = opponent_aces / opponent_points

    receive_pos = TennisGetVector3("Receive Stance")
    #avg_scoring_pos = TennisGetVector3("Opponent Average Scoring Location") # avg score position is the second bounce, not the first

    #r2avg_vec = avg_scoring_pos-receive_pos

    # Also here we might want to have a look at Estimated Opponent Shot Location (if not too easily manipulated) 

    return receive_pos #+ ace_pct * r2avg_vec

def serving_move_controller():
    return TennisGetVector3("Serve Stance")