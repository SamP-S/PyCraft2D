from math import *
import random as r
from blocks import *
from core import *
from state import *

class Chunk:

    WIDTH = 2**5
    HEIGHT = 2**6

    def __init__(self, x, blocks):
        self.x = x
        self.blocks = blocks

class World(Entity):
    
    # CONSTS
    SIZE = 4
    MIN_X, MAX_X = -(SIZE // 2) * Chunk.WIDTH, (SIZE // 2) * Chunk.WIDTH - 1    # inclusive
    MIN_Y, MAX_Y = 0, Chunk.HEIGHT - 1                                          # inclusive
    RANGE_X, RANGE_Y = MAX_X - MIN_X + 1, MAX_Y - MIN_Y + 1
    
    def __init__(self):
        super().__init__()
        self.name = "Default World"
        self.seed = r.randint(0, 1000)
        self.generator = "flat"
        self.gen_config = {}
        self.chunks = []
        for k in range(World.SIZE):
            blocks = [0] * Chunk.WIDTH * Chunk.HEIGHT
            chunk = Chunk((k - World.SIZE // 2) * Chunk.WIDTH, blocks)
            self.chunks.append(chunk)
        self._gen_flat()
            
    def get_block(self, x, y):
        assert(x >= World.MIN_X and x <= World.MAX_X)
        assert(y >= World.MIN_Y and y <= World.MAX_Y)
        
        chunk_idx = (x + World.RANGE_X // 2) // Chunk.WIDTH
        chunk_x = x % Chunk.WIDTH
        return self.chunks[chunk_idx].blocks[y * Chunk.WIDTH + chunk_x]

    def set_block(self, x, y, block_id):
        assert(x >= World.MIN_X and x <= World.MAX_X)
        assert(y >= World.MIN_Y and y <= World.MAX_Y)
        
        chunk_idx = (x + World.RANGE_X // 2) // Chunk.WIDTH
        chunk_x = x % Chunk.WIDTH
        self.chunks[chunk_idx].blocks[y * Chunk.WIDTH + chunk_x] = block_id
    
    def fill_blocks(self, ox, oy, dx, dy, block_id):
        assert(ox >= World.MIN_X and ox <= World.MAX_X)
        assert(oy >= World.MIN_Y and oy <= World.MAX_Y)
        assert(dx >= World.MIN_X and dx <= World.MAX_X)
        assert(dy >= World.MIN_Y and dy <= World.MAX_Y)
        
        dir_x, dir_y = 1 if ox < dx else -1, 1 if oy < dy else -1
        for y in range(oy, dy + dir_y, dir_y):
            for x in range(ox, dx + dir_x, dir_x):
                self.set_block(x, y, block_id)
                
    def _gen_flat(self):
        self.fill_blocks(World.MIN_X, 0, World.MAX_X, 0, State.R_BLOCKS["bedrock"])
        self.fill_blocks(World.MIN_X, 1, World.MAX_X, 14, State.R_BLOCKS["dirt"])
        self.fill_blocks(World.MIN_X, 15, World.MAX_X, 15, State.R_BLOCKS["grass"])
    
    def _gen_std(self):
        pass
    
    def draw(self, layer):
        # get viewport world bounds
        wx1, wy1, wx2, wy2 = State.CAMERA.get_viewport_bounds()
        wx1, wy1 = max(floor(wx1), World.MIN_X), max(floor(wy1), World.MIN_Y)
        wx2, wy2 = min(ceil(wx2), World.MAX_X), min(ceil(wy2), World.MAX_Y)
        
        # draw range
        for j in range(wy1, wy2 + 1):
            for i in range(wx1, wx2 + 1):
                block_id = self.world.get_block(i, j)
                x1, y1 = State.CAMERA.world_to_screen(i, j)
                x2, y2 = State.CAMERA.world_to_screen(i + 1, j + 1)
                
                pg.draw.rect(
                    layer, 
                    Block.BLOCKS[block_id].colour,
                    (
                        x1, y2,
                        x2 - x1, y1 - y2
                    )
                )

if __name__ == "__main__":
    world = World()
    world.set_block(0, 0, 1)
    world.set_block(0, 1, 2)
    world.set_block(1, 0, 3)
    world.set_block(World.MIN_X, 0, 1)
    world.set_block(World.MAX_X, 0, 1)
    world.set_block(0, World.MIN_Y, 1)
    world.set_block(0, World.MAX_Y, 1)
    world.fill_blocks(32, 4, 63, 7, 1)