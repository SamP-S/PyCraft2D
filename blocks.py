import pygame as pg
from enum import Enum
from state import *

# game constants
PIXEL_PER_SQUARE = 32

# block data structure
class Block:
    
    class BreakTime:
        default = True
        wood = True
        stone = True
        iron = True
        gold = True
        diamond = True
        shears = True
        sword = True
             
    def __init__(self, id, name, colour, is_outlined=True, breaktime=BreakTime()):
        self.id = id
        self.name = name
        self.colour = colour
        self.is_outlined = is_outlined
        self.breaktime = breaktime
        State.R_BLOCKS[name] = id

    def __repr__(self):
        return f"{self.name}({self.id})"
       
    @classmethod
    def find_block(cls, name):
        for block in cls.BLOCKS:
            if block.name == name:
                return block
        return None

# block constants as a class member variable
Block.BLOCKS = [
    Block(
        id=0, 
        name="air",
        colour=(255, 255, 255, 0),
        is_outlined=False,
    ),
    Block(1, "dirt", pg.color.THECOLORS["saddlebrown"]),
    Block(2, "stone", pg.color.THECOLORS["grey"], is_outlined=False,),
    Block(3, "wood", pg.color.THECOLORS["brown"]),
    Block(4, "leaves", pg.color.THECOLORS["green"],),
    Block(5, "bedrock", pg.color.THECOLORS["black"],),
    Block(6, "grass", pg.color.THECOLORS["green"]),
]
