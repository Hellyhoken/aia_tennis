from AIGamePyLibrary.AIGamePyLibrary import *


#Legal ball positions
#0,0,-6
#0,0,6
#14,0,6
#14,0,-6

def get_corners():
    is_home = TennisGetBool("Is Home")
    return [ConditionalSetVector3(is_home,Vector3(1.5,0,4),Vector3(-1.5,0,-4)),
     ConditionalSetVector3(is_home,Vector3(1.5,0,-4),Vector3(-1.5,0,4)),
     ConditionalSetVector3(is_home,Vector3(12.5,0,3.5),Vector3(-12.5,0,-3.5)),
     ConditionalSetVector3(is_home,Vector3(12.5,0,-3.5),Vector3(-12.5,0,3.5)),
     ]


    




def old_aim_controller():
    offset = Vector3(0,0.5,0)
    target = TennisGetVector3("Legal Serve Target")
    debug = DebugDrawDisc(target+offset, 0.5, 0.5, "Green")

    aim_target = TennisAutoAim(target)

    aim_debug = DebugDrawDisc(aim_target+offset, 0.5, 0.5, "Blue")
    return aim_target






def aim_away_controller():


    corners = get_corners()
    opponent_pos = RelativePosition(TennisGetTransform("Opponent"),"Self")

    #DebugDrawDisc(corners[0], 0.5, 0.5, "Blue")
    #DebugDrawDisc(corners[1], 0.5, 0.5, "Red")
    #DebugDrawDisc(corners[2], 0.5, 0.5, "Yellow")
    #DebugDrawDisc(corners[3], 0.5, 0.5, "Hot Pink")

    Distances = [Distance(corners[0],opponent_pos),
                 Distance(corners[1],opponent_pos),
                 Distance(corners[2],opponent_pos),
                 Distance(corners[3],opponent_pos)]

    hit_corner = corners[0]
    max_dist = -1

    hit_corner = ConditionalSetVector3(Distances[0]>max_dist,corners[0],hit_corner)
    max_dist = ConditionalSetFloat(Distances[0]>max_dist,Distances[0],max_dist)
    corner_number = 0

    hit_corner = ConditionalSetVector3(Distances[1]>max_dist,corners[1],hit_corner)
    max_dist = ConditionalSetFloat(Distances[1]>max_dist,Distances[1],max_dist)
    corner_number = ConditionalSetVector3(Distances[1]>max_dist,1,corner_number)

    hit_corner = ConditionalSetVector3(Distances[2]>max_dist,corners[2],hit_corner)
    max_dist = ConditionalSetFloat(Distances[2]>max_dist,Distances[2],max_dist)
    corner_number = ConditionalSetVector3(Distances[1]>max_dist,2,corner_number)

    hit_corner = ConditionalSetVector3(Distances[3]>max_dist,corners[3],hit_corner)
    max_dist = ConditionalSetFloat(Distances[3]>max_dist,Distances[3],max_dist)
    corner_number = ConditionalSetVector3(Distances[1]>max_dist,3,corner_number)

    SetVariable("hitting_corner", corner_number)
    SetVariable("corner_to_hit",hit_corner)

    is_home = TennisGetBool("Is Home")

    _,_,z_pos = Vector3Split(RelativePosition(TennisGetTransform("Self"),"Self"))
    z_pos = ConditionalSetFloat(is_home,z_pos,MultiplyFloats(z_pos,-1))



    hit_corner = ConditionalSetVector3(CompareBool(hit_corner == 0,z_pos>3.5,"and"),corners[1],hit_corner)
    hit_corner = ConditionalSetVector3(CompareBool(hit_corner == 1,z_pos<-3.5,"and"),corners[0],hit_corner)
    

  
    debug = DebugDrawDisc(hit_corner, 0.5, 0.5, "Green")

    return TennisAutoAim(hit_corner)





