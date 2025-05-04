import pygame as pg
from core import *
from state import *

class Cursor(Entity):
    
    def __init__(self):
        super().__init__()
    
    def update(self, dt):
        self.x, self.y = State.CAMERA.screen_to_world(pg.mouse.get_pos())
        
    def draw(self):
        pass
