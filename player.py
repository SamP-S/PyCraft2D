import pygame as pg
from math import *
from core import *

class Player(Entity):
    
    MAX_SPEED = 4.0
    
    def __init__(self, name: str):
        super().__init__()
        self.name:str = name
        self.dx:float = 0.0
        self.dy:float = 0.0
        
        
    def update(self, dt):
        # get velocity
        dx, dy = 0, 0
        if pg.key.get_pressed()[pg.K_w]:
            dy += self.MAX_SPEED
        elif pg.key.get_pressed()[pg.K_s]:
            dy -= self.MAX_SPEED
        elif pg.key.get_pressed()[pg.K_a]:
            dx -= self.MAX_SPEED
        elif pg.key.get_pressed()[pg.K_d]:
            dx += self.MAX_SPEED
        self.x += dx * dt
        self.y += dy * dt
        
    def draw(self, dt):
        pass

    def __str__(self):
        return f"{self.name}({self.x}, {self.y})"
