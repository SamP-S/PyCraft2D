import time
import os
import pygame as pg
from Blocks import *
from Player import *
from math import *
from Constants import *
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
        pg.display.set_caption("Pycraft2D")
        self.clock = pg.time.Clock()
        self.running = True
        self.world = gen_world()
        self.player = Player("Steve")        
        
        # set player start position
        self.player.x = 0
        for j in range(CHUNK_HEIGHT-1, -1, -1):
            if self.world[j][0] != 0:
                self.player.y = j
                self.player.y_cache = j
                break
            

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    
            self.screen.fill((255, 255, 255))
            self.player.update()
            self.draw_world()
            pg.display.flip()
            self.clock.tick(60)
        pg.quit()
        
        
    def draw_world(self):
        # draw chunk
        for y, row in enumerate(self.world):
            for x, block_id in enumerate(row):           
                print(self.screen.get_rect())    
                # draw block
                pg.draw.rect(
                    self.screen, 
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
                        self.screen, 
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
