import time
import os
import pygame as pg
from blocks import *
from player import *
from math import *
import random as r
from world import *
from cursor import *
from camera import *
from state import *


class App:
    
    def __init__(self):
        # initialisation
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.world_surf = pg.Surface(self.screen.get_size(), flags=pg.SRCALPHA)
        pg.display.set_caption("Pycraft2D")
        self.clock = pg.time.Clock()
        self.exit_flag = False
        
        self.block_atlas = pg.image.load(os.path.join("assets", "blocks.png"))
        self.steve_skin = pg.image.load(os.path.join("assets", "steve.png"))
        
        # set up camera
        State.CAMERA = Camera()
        
        # entities
        State.world = World()
        State.player = Player("Steve")
        State.cursor = Cursor()
        State.CAMERA.target = State.player
        
        # set player start position
        State.player.x = 0
        for j in range(Chunk.HEIGHT-1, -1, -1):
            if State.world.get_block(State.player.x, j) != 0:
                State.player.y = j + 1
                break

    def run(self):
        while self.exit_flag == False:
            # get delta time
            dt = self.clock.tick() / 1000.0
            
            # event handling
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.WINDOWCLOSE:
                    self.exit_flag = True
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.exit_flag = True
                elif event.type == pg.WINDOWRESIZED:
                    print(f"{event.type} ({event.x} {event.y})")
                elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                    print(f"{event.type} ({event.pos[0]} {event.pos[1]} {event.button})")
                elif event.type == pg.MOUSEMOTION:
                    pass
            
            # main loop
            State.player.update(dt)
            State.cursor.update(dt)
            
            # draw calls
            self.screen.fill((100, 240, 255, 255))
            self.world_surf.fill((0, 0, 0, 0))
            
            State.world.draw(self.world_surf)
            State.player.draw(self.world_surf)
            State.cursor.draw(self.world_surf)
            
            self.screen.blit(self.world_surf, (0, 0))
            self.screen.blit(self.block_atlas, (0, 0), (0, 0, 512, 512))
            pg.display.flip()
            
        # cleanup
        pg.display.quit()
        pg.quit()
        

if __name__ == "__main__":
    print("main pycraft")
    print(pg.color.THECOLORS["white"])
    app = App()
    app.run()
