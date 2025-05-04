from math import *
import pygame as pg
from core import *
from state import *

class Cursor(Entity):
    
    def __init__(self):
        super().__init__()
        self.colour = (0, 0, 0)
        self.width = 1
    
    def update(self, dt):
        cx, cy = pg.mouse.get_pos()
        self.x, self.y = State.CAMERA.screen_to_world(cx, cy)
        self.x, self.y = floor(self.x), floor(self.y)
        
    def draw(self, layer):
        assert(layer is not None)
        assert(isinstance(self.colour, tuple) and len(self.colour) == 3)
        assert(self.width > 0)
        sr = State.CAMERA.world_to_screen_rect(self.x, self.y, 1, 1)
        pg.draw.rect(layer, self.COLOUR, sr, width=self.width)
