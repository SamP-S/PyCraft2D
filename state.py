
class State:
    
    # registers
    R_WORLD_GENERATORS: dict = {}
    R_BLOCKS: dict = {}
    
    # singletons
    CAMERA = None
    
    # entities  
    world = None
    player = None
    cursor = None
