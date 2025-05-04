from math import *
import pygame as pg
from core import *
from state import *

class Cursor(Entity):
    
    def __init__(self):
        super().__init__()
    
    def update(self, dt):
        cx, cy = pg.mouse.get_pos()
        self.x, self.y = State.CAMERA.screen_to_world(cx, cy)
        self.x, self.y = floor(self.x), floor(self.y)
        
    def draw(self):
        pass
