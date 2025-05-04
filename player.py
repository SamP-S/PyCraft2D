import pygame as pg
from math import *
from core import *
from state import *

class Player(Entity):
    
    MAX_SPEED = 4.0
    
    def __init__(self, name:str):
        super().__init__()
        self.name:str = name
        self.dx:float = 0.0
        self.dy:float = 0.0
        # draw
        self.colour:tuple[int, int, int] = (0, 255, 0)
        
    def update(self, dt:float):
        # get velocity
        dx, dy = 0, 0
        if pg.key.get_pressed()[pg.K_w]:
            dy += Player.MAX_SPEED
        elif pg.key.get_pressed()[pg.K_s]:
            dy -= Player.MAX_SPEED
        elif pg.key.get_pressed()[pg.K_a]:
            dx -= Player.MAX_SPEED
        elif pg.key.get_pressed()[pg.K_d]:
            dx += Player.MAX_SPEED
        self.x += dx * dt
        self.y += dy * dt
        
    def draw(self, layer):
        assert(layer is not None)
        assert(isinstance(self.colour, tuple) and len(self.colour) == 3)
        # draw player
        sr = State.CAMERA.world_to_screen_rect(self.x, self.y, 1, 1)
        pg.draw.rect(layer, Player.COLOUR, sr)
