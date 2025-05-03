import pygame as pg
from core import *

class Cursor(Entity):
    
    def __init__(self):
        super().__init__()
        self.player = None
    
    def update(self, dt):
        cx, cy = pg.mouse.get_pos()
        if self.player is None:
            print("Cursor has no player")
        else:
            window_width = pg.display.get_surface().get_width()
            self.x = ((cx + self.player.x) // 32) * 32
            self.y = ((cy + self.player.y) // 32) * 32
        
    def draw(self):
        pass
