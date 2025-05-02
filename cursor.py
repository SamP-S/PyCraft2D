import pygame as pg

class Cursor:
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.player = None
    
    def update(self, dt):
        cursor_pos = pg.mouse.get_pos()
        if self.player is None:
            print("Cursor has no player")
        else:
            window_width = pg.display.get_surface().get_width()
            self.x = self.player.x - (window_width // 2) + cursor_pos[0]
            self.y = self.player.y - (window_width // 2) + cursor_pos[1]
        
    def draw(self):
        pass
