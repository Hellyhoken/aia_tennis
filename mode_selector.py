from AIGamePyLibrary.AIGamePyLibrary import *

def mode_selector():
    return [
        SetVariable("serving", False),
        SetVariable("receiving_serve", False),
        SetVariable("recieving", False), # possibly divide into lob, flat or charged
        SetVariable("awaiting_opponet_hit", False) # possibly divide into charged (cannot be returned as charged?) or not charged
    ]