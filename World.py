import random as r
from Blocks import *

# Summary: Chunk class
# Responsible for the data management of all the blocks in side a single chunk including:
# - storing the blocks in a 1D array
# - storing the chunk position in the world

class Chunk:
    
    CHUNK_WIDTH = 32
    CHUNK_HEIGHT = 64
    
    def __init__(self, x, blocks):
        self.x = x
        self.blocks = [0] * (Chunk.CHUNK_WIDTH * Chunk.CHUNK_HEIGHT)
        

# Summary: World class
# Responsible for management of all chunks in the world including:
# - generating the world using seed num. (height, trees, ore veins, water, etc.)
# - loading/unloading chunks according to player position
# - storing changes in the world

class World:
    
    WORLD_SIZE = 4

    
    def __init__(self):
        self.chunks = []
        self.generate_world()

    # TODO: use seed
    def generate(self):
    
        self.chunks = []
        for k in range(World.WORLD_SIZE):
            
            # create chunk
            blocks = []
            for j in range(World.CHUNK_HEIGHT):
                for i in range(World.CHUNK_WIDTH):
                    if j < World.CHUNK_HEIGHT // 2:
                        blocks.append(r.randint(1, MAX_BLOCK))
                    else:
                        blocks.append(0)
            self.chunks.append(Chunk(k * Chunk.CHUNK_WIDTH, blocks))
        
    def draw(self):
        pass
