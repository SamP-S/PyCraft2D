from abc import ABC, abstractmethod
from state import State
from world import World, Chunk

# immutable settings required before world generation
class WorldConfig:
        
    def __init__(self):
        self.name = "Default World"
        self.seed = 0
        self.generator = "flat"
        self.gen_config = {}

class WorldGenerator(ABC):
    
    @abstractmethod
    def get_gen_config(self):
        pass
    
    @abstractmethod
    def generate(self, world_config):
        pass
    

class FlatWorldGenerator(WorldGenerator):
    
    def get_gen_config(self):
        return {
            "fill_height": 16,
        }
    
    def generate(self, world_config):
        world = World()
        for k in range(world.WORLD_SIZE):
            blocks = [0] * Chunk.WIDTH * Chunk.CHUNK_HEIGHT
            chunk = Chunk((k - world.WORLD_SIZE // 2 - 1) * Chunk.CHUNK_WIDTH, blocks)
            world.chunks.append(chunk)
            
        # generate blank world
        self.chunks = []
        for k in range(World.WORLD_SIZE):
            blocks = [0] * Chunk.CHUNK_WIDTH * Chunk.CHUNK_HEIGHT
            chunk = Chunk((k - World.WORLD_SIZE // 2 - 1) * Chunk.CHUNK_WIDTH, blocks)
            self.chunks.append(chunk)
            
class StandardWorldGenerator(WorldGenerator):
    
    def get_gen_config(self):
        return {
            "seed": 0,
        }
    
    def generate(self, world_config):
        pass

State.R_WORLD_GENERATORS.append(FlatWorldGenerator())
State.R_WORLD_GENERATORS.append(StandardWorldGenerator())
