import pygame as pg

# game constants
PIXEL_PER_SQUARE = 32

# block data structure
class Block:
    def __init__(self, id, name, colour, is_outlined=True):
        self.id = id
        self.name = name
        self.colour = colour
        self.is_outlined = is_outlined
        
        # block constants
        self.BLOCKS = [
            Block(0, "air", (255, 255, 255, 0), False),
            Block(1, "dirt", pg.color.THECOLORS["saddlebrown"]),
            Block(2, "stone", pg.color.THECOLORS["grey"]),
            Block(3, "wood", pg.color.THECOLORS["brown"]),
            Block(4, "leaves", pg.color.THECOLORS["green"]),
            Block(5, "bedrock", pg.color.THECOLORS["black"]),
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
    



