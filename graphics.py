from math import *
import pygame as pg
from state import *

class Drawable:
    
    def __init__(self):
        pass

    def draw(self):
        pass
    
class Rect(Drawable):
    
    def __init__(self, x=0, y=0, w=1, h=1, color=(255, 255, 255, 255)):
        super().__init__()
        # dimensions
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        # colour
        self.color = color
        # border
        self.border = 1
        self.border_color = (0, 0, 0, 255)
    
    def draw(self, layer):
        super().draw()
        
        assert(State.CAMERA is not None)
        assert(layer is not None)
        assert(self.border >= 0)
        
        # draw filled rect
        pg.draw.rect(
            layer, self.color, 
            State.CAMERA.world_to_screen_rect(self.x, self.y, self.w, self.h),
        )
        # draw border
        if self.border > 0:
            pg.draw.rect(
                layer, self.border_color, 
                State.CAMERA.world_to_screen_rect(self.x, self.y, self.w, self.h),
                width=self.border
            )
