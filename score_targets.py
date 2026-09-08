from AIGamePyLibrary.AIGamePyLibrary import *
from trajectory_predicter import INTERCEPT_POINT
from params import AIM_X_COORDS, MOVE_TARGETS, SHOT_SPEEDS, TARGETS
from utils import max_float, max_vector3, min_vector3, squash_axes, squash_y_axis

DEFAULT_SHOT = TennisGetFloat("Shot: Slice")
DEFAULT_SHOT_SPEED = SHOT_SPEEDS["Flat"]

def get_height_over_at_net():
    fn = CreateFunction("get_height_over_at_net")
    target, intersection_point = fn.Param1, fn.Param2
    zero = AssignToFunction(Float(0), fn)
    g = AssignToFunction(Float(28), fn)
    target_x,_,target_z = Vector3Split(target)
    target_x = AssignToFunction(target_x, fn)
    target_z = AssignToFunction(target_z, fn)
    abs_target_x = AssignToFunction(Abs(target_x), fn)
    intersection_x,intersection_y,intersection_z = Vector3Split(intersection_point)
    intersection_x = AssignToFunction(intersection_x, fn)
    intersection_y = AssignToFunction(intersection_y, fn)
    intersection_z = AssignToFunction(intersection_z, fn)

    diff_x = AssignToFunction(target_x - intersection_x, fn)
    diff_z = AssignToFunction(target_z - intersection_z, fn)
    dist_x = AssignToFunction(Abs(diff_x), fn)

    net_height = AssignToFunction(TennisGetFloat("Net Height"), fn)

    div_x = AssignToFunction(DivideFloats(abs_target_x, dist_x), fn)
    los_height = AssignToFunction(intersection_y * div_x, fn)

    target_vec = AssignToFunction(Vector3(diff_x, zero, diff_z), fn)
    target_dist = AssignToFunction(Magnitude(target_vec), fn)
    net_dist = AssignToFunction(MultiplyFloats(target_dist, div_x), fn)

    lb = AssignToFunction(MultiplyFloats(g, net_dist), fn)
    lb1 = AssignToFunction(SubtractFloats(target_dist, net_dist), fn)
    lb2 = AssignToFunction(MultiplyFloats(lb, lb1), fn)
    speed = AssignToFunction(Float(SHOT_SPEEDS["Flat"]), fn)
    two = AssignToFunction(Float(2), fn)
    pow = AssignToFunction(Power(speed, two), fn)
    den = AssignToFunction(MultiplyFloats(two, pow), fn)
    gravity_drop_lower_bound = AssignToFunction(DivideFloats(lb2, den), fn)

    y_net_est = AssignToFunction(AddFloats(los_height, gravity_drop_lower_bound), fn)
    height_over_net = AssignToFunction(y_net_est - net_height, fn)
    abs_height_over_net = AssignToFunction(Abs(height_over_net), fn)

    return SetFunctionReturn(fn, abs_height_over_net)
    

def pick_target_from_list():
    fn = CreateFunction("pick_target_from_list")
    intersection_point, z_dir = fn.Param1, fn.Param2

    mo = AssignToFunction(Float(-1), fn)
    one = AssignToFunction(Float(1), fn)
    six = AssignToFunction(Float(6), fn)

    side = AssignToFunction(TennisGetBool("Is Home"), fn)
    side_float = AssignToFunction(ConditionalSetFloat(side, one, mo), fn)

    z_coord = AssignToFunction(MultiplyFloats(six, z_dir), fn)

    targets = []
    heights = []
    for x in AIM_X_COORDS:
        x_coord = AssignToFunction(Float(x), fn)
        x_coord = AssignToFunction(x_coord * side_float, fn)
        target = AssignToFunction(Vector3(x_coord, 0, z_coord), fn)
        targets.append(target)
        height = AssignToFunction(CustomFunction("get_height_over_at_net", target, intersection_point), fn)
        heights.append(height)

    min_vector = targets[0]
    min_float = heights[0]
    for i in range(1, len(targets)):
        smallest = AssignToFunction(CompareFloats(heights[i], min_float, "<"), fn)
        min_vector = AssignToFunction(ConditionalSetVector3(
            smallest,
            targets[i],
            min_vector
        ), fn)
        min_float = AssignToFunction(ConditionalSetFloat(
            smallest,
            heights[i],
            min_float
        ), fn)

    return SetFunctionReturn(fn, min_vector)

def score_target():
    fn = CreateFunction("score_target")
    target, intersection_point, opponent_pos = fn.Param1, fn.Param2, fn.Param3

    one = AssignToFunction(Float(1.0), fn)

    i2t = AssignToFunction(SubtractVector3(intersection_point, target), fn)
    i2t_mag = AssignToFunction(Magnitude(i2t), fn)
    i2t_inv_mag = AssignToFunction(DivideFloats(one, i2t_mag), fn)
    i2t_norm = AssignToFunction(ScaleVector3(i2t, i2t_inv_mag), fn)

    i2o = AssignToFunction(SubtractVector3(intersection_point, opponent_pos), fn)
    recv_t = AssignToFunction(DotProduct(i2o, i2t_norm), fn)
    recv_offset = AssignToFunction(ScaleVector3(i2t_norm, recv_t), fn)
    recv_pos = AssignToFunction(AddVector3(intersection_point, recv_offset), fn)

    recv_diff = AssignToFunction(SubtractVector3(recv_pos, opponent_pos), fn)
    recv_dist = AssignToFunction(Magnitude(recv_diff), fn)

    score = AssignToFunction(DivideFloats(recv_dist, recv_t), fn)

    return SetFunctionReturn(fn, score)

_ = get_height_over_at_net()
_ = pick_target_from_list()
_ = score_target()

def score_aim_targets(opponent_pos):
    target1 = CustomFunction("pick_target_from_list", INTERCEPT_POINT, -1)
    target2 = CustomFunction("pick_target_from_list", INTERCEPT_POINT, 1)

    _ = DebugDrawDisc(target1, 0.5, 0.5, "Green")
    _ = DebugDrawDisc(target2, 0.5, 0.5, "Green")

    target1_score = CustomFunction("score_target", target1, INTERCEPT_POINT, opponent_pos)
    target2_score = CustomFunction("score_target", target2, INTERCEPT_POINT, opponent_pos)

    _ = DebugDrawLine(target1, AddVector3(target1, Vector3(0, target1_score, 0)), 0.5, "Blue")
    _ = DebugDrawLine(target2, AddVector3(target2, Vector3(0, target2_score, 0)), 0.5, "Blue")

    best_target = ConditionalSetVector3(
        CompareFloats(target1_score, target2_score, ">"),
        target1,
        target2
    )

    opp_x, _, _ = Vector3Split(opponent_pos)
    _, _, int_z = Vector3Split(INTERCEPT_POINT)
    opp_close = Abs(opp_x) < 5.0
    in_field = Abs(int_z) < 6.0

    do_lob = CompareBool(opp_close, in_field)

    best_target = ConditionalSetVector3(
        do_lob,
        Vector3(13.9 * ConditionalSetFloat(TennisGetBool("Is Home"), 1.0, -1.0), 0, int_z),
        best_target
    )
    shot_type = ConditionalSetFloat(
        do_lob,
        TennisGetFloat("Shot: Lob"),
        TennisGetFloat("Shot: Slice")
    )
    return best_target, shot_type

def aim_target():
    opponent_pos = RelativePosition(TennisGetTransform("Opponent"), "Self")
    return score_aim_targets(opponent_pos)
AIM_TARGET, SHOT_TYPE = aim_target()

