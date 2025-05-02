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
        world.fill_blocks(World.MIN_X, 0, World.MAX_X, 0, State.R_BLOCKS["bedrock"])
        world.fill_blocks(World.MIN_X, 1, World.MAX_X, 14, State.R_BLOCKS["dirt"])
        world.fill_blocks(World.MIN_X, 15, World.MAX_X, 15, State.R_BLOCKS["grass"])
        return world
            
class StandardWorldGenerator(WorldGenerator):
    
    def get_gen_config(self):
        return {
            "seed": 0,
        }
    
    def generate(self, world_config):
        pass


def create_world(world_config):
    gen = State.R_WORLD_GENERATORS[world_config.generator]
    return gen.generate(world_config)

State.R_WORLD_GENERATORS["flat"] = FlatWorldGenerator()
State.R_WORLD_GENERATORS["standard"] = StandardWorldGenerator()
