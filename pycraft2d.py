import time
import os
import pygame as pg
from blocks import *
from player import *
from math import *
import random as r
from world import *
from generator import *
from cursor import *


class App:
    
    def __init__(self):
        # initialisation
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        print(self.screen.get_size())
        self.world_surf = pg.Surface(self.screen.get_size(), flags=pg.SRCALPHA)
        pg.display.set_caption("Pycraft2D")
        self.clock = pg.time.Clock()
        self.exit_flag = False
        self.world_config = WorldConfig()
        self.world = create_world(self.world_config)
        self.player = Player("Steve")
        self.cursor = Cursor()
        self.cursor.player = self.player
        
        # set player start position
        self.player.x = 0
        for j in range(Chunk.HEIGHT-1, -1, -1):
            if self.world.get_block(self.player.x, j) != 0:
                self.player.y = j + 1
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
                    print(f"{event.type} {event.w} {event.h}")
                elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                    pass
                elif event.type == pg.MOUSEMOTION:
                    pass
            
            # main loop
            self.player.update(dt)
            self.cursor.update(dt)
            
            # draw calls
            self.screen.fill((100, 240, 255, 255))
            self.draw_world()
            pg.draw.rect(
                self.world_surf,
                pg.color.THECOLORS["black"], 
                (
                    self.cursor_pos[0], 
                    self.cursor_pos[1],  
                    PIXEL_PER_SQUARE, 
                    PIXEL_PER_SQUARE
                ),
                width=1
            )
            
            self.screen.blit(self.world_surf, (0, 0))
            pg.display.flip()
            
        # cleanup
        pg.display.quit()
        pg.quit()
        
    def draw_world(self):
        # draw chunk
        for k, chunk in enumerate(self.world.chunks):
            for pos, block_id in enumerate(chunk.blocks):
                y = pos // Chunk.WIDTH
                x = pos - y * Chunk.WIDTH                    # draw block
                pg.draw.rect(
                    self.world_surf, 
                    Block.BLOCKS[block_id].colour,
                    (
                        self.screen.get_rect()[2] // 2 + (x - self.player.x) * PIXEL_PER_SQUARE, 
                        self.screen.get_rect()[3] // 2 - (y - self.player.y) * PIXEL_PER_SQUARE,  
                        PIXEL_PER_SQUARE, 
                        PIXEL_PER_SQUARE
                    )
                )

if __name__ == "__main__":
    print("main pycraft")
    print(pg.color.THECOLORS["white"])
    app = App()
    app.run()
