import random as r
from Blocks import *

class World:
    
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
    
    def __init__(self):
        self.world = []
        self.chunk_width = CHUNK_WIDTH
        self.chunk_height = CHUNK_HEIGHT
        self.max_block = MAX_BLOCK
        self.generate_world()

    def generate_world(self):
        self.world = []
        for j in range(self.chunk_height):
            row = []
            for i in range(self.chunk_width):
                if j < self.chunk_height // 2:
                    row.append(r.randint(1, self.max_block))
                else:
                    row.append(0)
            self.world.append(row)
            
            

    def draw(self):
        pass
