from AIGamePyLibrary.AIGamePyLibrary import *

from utils import squash_y_axis

G = 27

def kast_parabel():
    ball_position = TennisGetVector3("Ball Position")
    ball_velocity = TennisGetVector3("Ball Velocity")

    _, ball_y, _ = Vector3Split(ball_position)
    _, vy, _ = Vector3Split(ball_velocity)
    vh = Magnitude(squash_y_axis(ball_velocity))

    current_bounce_lim1, current_bounce_lim2, cbt1, cbt2 = solve_one_bounce(ball_y, vy, vh)

    vl1 = SetVariable("height_limit1_start", current_bounce_lim1)
    vl2 = SetVariable("height_limit1_end", current_bounce_lim2)
    vl1t = SetVariable("height_limit1_start_time", cbt1)
    vl2t = SetVariable("height_limit1_end_time", cbt2)

    gbt1, gbt2 = solve_for_height(ball_y, vy, 0)
    gbt = gbt1 + gbt2
    gbp = gbt * vh

    vy_pre_bounce = vy + gbt*-G

    topspin = TennisGetBool("Was Last Shot Topspin")

    vy_k = ConditionalSetFloat(topspin, -1.05, -0.75)
    vy_m = ConditionalSetFloat(topspin, 2, 1)

    vh_k = ConditionalSetFloat(topspin, 1.1, 0.95)

    vy_post_bounce = vy_k * vy_pre_bounce + vy_m

    vh_post_bounce = vh_k * vh

    after_bounce_lim1, after_bounce_lim2, abt1, abt2 = solve_one_bounce(0, vy_post_bounce, vh_post_bounce)

    vbl1 = SetVariable("height_limit2_start", gbp + after_bounce_lim1)
    vbl2 = SetVariable("height_limit2_end", gbp + after_bounce_lim2)
    vbl1t = SetVariable("height_limit2_start_time", gbt + abt1)
    vbl2t = SetVariable("height_limit2_end_time", gbt + abt2)

def solve_one_bounce(y0, vy0, vh):
    term1, term2 = solve_for_height(y0, vy0, 5)

    t1 = term1 - term2
    t2 = term1 + term2

    lim1 = t1 * vh
    lim2 = t2 * vh

    return lim1, lim2, t1, t2


def solve_for_height(y0, vy0, target_height):
    pd2 = vy0 / G
    q = (y0 - target_height) / (G/2)

    determinant = pd2**2+q

    return pd2, Operation(determinant, "sqrt")
    