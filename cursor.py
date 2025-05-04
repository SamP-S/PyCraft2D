import pygame as pg
from core import *
from state import *

class Cursor(Entity):
    
    def __init__(self):
        super().__init__()
    
    def update(self, dt):
        cx, cy = pg.mouse.get_pos()
        self.x, self.y = State.CAMERA.screen_to_world(cx, cy)
        
    def draw(self):
        pass
