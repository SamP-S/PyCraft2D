import pygame as pg
from enum import Enum

# game constants
PIXEL_PER_SQUARE = 32

# block data structure
class Block:
    
    class Breakability(Enum):
        GAS = 0
        LIQUID = 1
        SOFT = 2
        REGULAR = 3
        STONE = 4
        IRON = 5
        GOLD = 6
        DIAMOND = 7
        UNBREAKABLE = 8
             
    def __init__(self, id, name, colour, is_outlined=True, breakability=Breakability.REGULAR):
        self.id = id
        self.name = name
        self.colour = colour
        self.is_outlined = is_outlined
        self.breakability = breakability
        
        # block constants
        self.BLOCKS = [
            Block(
                id=0, 
                name="air",
                colour=(255, 255, 255, 0),
                is_outlined=False, 
                breakability=Block.Breakability.GAS
            ),
            Block(1, "dirt", pg.color.THECOLORS["saddlebrown"]),
            Block(2, "stone", pg.color.THECOLORS["grey"], is_outlined=False, breakability=Block.Breakability.STONE),
            Block(3, "wood", pg.color.THECOLORS["brown"]),
            Block(4, "leaves", pg.color.THECOLORS["green"], breakability=Block.Breakability.SOFT),
            Block(5, "bedrock", pg.color.THECOLORS["black"], breakability=Block.Breakability.UNBREAKABLE),
            Block(6, "grass", pg.color.THECOLORS["green"]),
        ]

    def __repr__(self):
        return f"Block(name={self.name}, texture={self.texture})"
    
    @classmethod
    def find_block(cls, name):
        for block in cls.BLOCKS:
            if block.name == name:
                return block
        return None
    



