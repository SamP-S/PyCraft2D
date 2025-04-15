import time
import os
import pygame as pg
from Blocks import *
from Player import *
from math import *
import random as r

def gen_world():
    world = []
    for j in range(CHUNK_HEIGHT):
        row = []
        for i in range(CHUNK_WIDTH):
            if j < CHUNK_HEIGHT // 2:
                row.append(r.randint(1, MAX_BLOCK))
            else:
                row.append(0)
        world.append(row)
    return world

class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        print(self.screen.get_size())
        self.world_surf = pg.Surface(self.screen.get_size(), flags=pg.SRCALPHA)
        pg.display.set_caption("Pycraft2D")
        self.clock = pg.time.Clock()
        self.exit_flag = False
        self.world = gen_world()
        self.player = Player("Steve")        
        
        # set player start position
        self.player.x = 0
        for j in range(CHUNK_HEIGHT-1, -1, -1):
            if self.world[j][0] != 0:
                self.player.y = j
                break
            

    def run(self):
        while self.exit_flag == False:
            # get delta time
            dt = self.clock.tick() / 1000.0
            
            # event handling
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.WINDOWCLOSE:
                    self.running = False
                elif event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                    print(f"{event.type} {event.key}")
                elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                    print(f"{event.type} {event.pos} {event.button}")
                elif event.type == pg.MOUSEMOTION:
                    print(f"{event.type} {event.pos} {event.rel} {event.buttons}")
                elif event.type == pg.WINDOWRESIZED:
                    print(f"{event.type} {event.w} {event.h}")
            
            # main loop
            self.screen.fill((100, 240, 255, 255))
            self.screen.blit(self.world_surf, (0, 0))
            self.player.update(dt)
            self.draw_world()
            pg.display.flip()
            
        # cleanup
        pg.display.quit()
        pg.quit()
        
        
    def draw_world(self):
        # draw chunk
        for y, row in enumerate(self.world):
            for x, block_id in enumerate(row): 
                # draw block
                pg.draw.rect(
                    self.world_surf, 
                    BLOCKS[block_id].colour,
                    (
                        self.screen.get_rect()[2] // 2 + (x - self.player.x) * PIXEL_PER_SQUARE, 
                        self.screen.get_rect()[3] // 2 - (y - self.player.y) * PIXEL_PER_SQUARE,  
                        PIXEL_PER_SQUARE, 
                        PIXEL_PER_SQUARE
                    )
                )
                
                # block outline
                if BLOCKS[block_id].is_outlined:
                    pg.draw.rect(
                        self.world_surf, 
                        pg.color.THECOLORS["black"], 
                        (
                            self.screen.get_rect()[2] // 2 + (x - self.player.x) * PIXEL_PER_SQUARE, 
                            self.screen.get_rect()[3] // 2 - (y - self.player.y) * PIXEL_PER_SQUARE,  
                            PIXEL_PER_SQUARE, 
                            PIXEL_PER_SQUARE
                        ),
                        width=1
                    )

if __name__ == "__main__":
    print("main pycraft")
    print(pg.color.THECOLORS["white"])
    app = App()
    app.run()
