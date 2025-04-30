from abc import ABC, abstractmethod
from State import State

# immutable settings required before world generation
class WorldConfig:
        
    def __init__(self):
        self.name = "Default World"
        self.generator = "flat"
        self.seed = 0

class WorldGenerator(ABC):
    
    @abstractmethod
    def get_config(self):
        pass
    
    @abstractmethod
    def generate(self, config):
        pass
    

class FlatWorldGenerator(WorldGenerator):
    
    def get_config(self):
        return {
            "name": "Flat World",
            "generator": "flat"
        }
    
    def generate(self, world):
        # Generate a flat world
        for k in range(world.WORLD_SIZE):
            blocks = [0] * Chunk.CHUNK_WIDTH * Chunk.CHUNK_HEIGHT
            chunk = Chunk((k - world.WORLD_SIZE // 2 - 1) * Chunk.CHUNK_WIDTH, blocks)
            world.chunks.append(chunk)
            
class StandardWorldGenerator(WorldGenerator):
    
    def get_config(self):
        return {
            "name": "Flat World",
            "generator": "flat"
        }
    
    def generate(self, world):
        # Generate a flat world
        for k in range(world.WORLD_SIZE):
            blocks = [0] * Chunk.CHUNK_WIDTH * Chunk.CHUNK_HEIGHT
            chunk = Chunk((k - world.WORLD_SIZE // 2 - 1) * Chunk.CHUNK_WIDTH, blocks)
            world.chunks.append(chunk)

State.R_WORLD_GENERATORS.append(StandardWorldGenerator())
State.R_WORLD_GENERATORS.append(FlatWorldGenerator())