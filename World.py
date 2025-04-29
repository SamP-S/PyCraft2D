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
        self.blocks = blocks
        
# Summary: World class
# Responsible for management of all chunks in the world including:
# - generating the world using seed num. (height, trees, ore veins, water, etc.)
# - loading/unloading chunks according to player position
# - storing changes in the world

class World:
    
    def __init__(self):
        self.chunks = []
        self.generate()

    # TODO: use seed
    def generate(self):
        # generate blank world
        self.chunks = []
        for k in range(World.WORLD_SIZE):
            blocks = [0] * Chunk.CHUNK_WIDTH * Chunk.CHUNK_HEIGHT
            chunk = Chunk((k - World.WORLD_SIZE // 2 - 1) * Chunk.CHUNK_WIDTH, blocks)
            self.chunks.append(chunk)
    
    @staticmethod    
    def generate_flat(world):
        pass

    # use seed & perlin noise
    @staticmethod
    def generate_std(world):
        pass
    
    # CONSTS
    # needs to be after funcs
    WORLD_SIZE = 4  
    WORLD_GENERATORS = {
        "flat" : generate_flat,
        "standard" : generate_std
    }
        
    
    def generate(self):
        self.blocks = [Block.find_block("air")] * (Chunk.CHUNK_WIDTH * Chunk.CHUNK_HEIGHT)
        self.blocks[0 : Chunk.CHUNK_WIDTH] = [5] * Chunk.CHUNK_WIDTH
        for j in range(1, Chunk.CHUNK_HEIGHT // 2 - 1):
            self.blocks[j * Chunk.CHUNK_WIDTH:(j+1) * Chunk.CHUNK_WIDTH] = [Block.find_block("dirt")] * Chunk.CHUNK_WIDTH
        self.blocks[0 : Chunk.CHUNK_WIDTH] = [Block.find_block("bedrock")] * Chunk.CHUNK_WIDTH
        
    def draw(self):
        pass
