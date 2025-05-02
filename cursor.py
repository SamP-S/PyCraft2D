import pygame as pg

class Cursor:
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.player = None
    
    def update(self, dt):
        cx, cy = pg.mouse.get_pos()
        if self.player is None:
            print("Cursor has no player")
        else:
            window_width = pg.display.get_surface().get_width()
            self.x = (cx // 32) * 32
            self.y = (cy // 32) * 32
        
    def draw(self):
        pass
