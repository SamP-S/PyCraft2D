
class Camera:
    
    PIXEL_PER_SQUARE = 32
    
    def __init__(self):
        self.x, self.y = 0, 0
        self.w, self.h = 0, 0
        self.target = None
        
        
