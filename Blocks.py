import pygame as pg

class Block:
    def __init__(self, id, name, colour, is_outlined=True):
        self.id = id
        self.name = name
        self.colour = colour
        self.is_outlined = is_outlined

    def __repr__(self):
        return f"Block(name={self.name}, texture={self.texture})"

BLOCKS = [
    Block(0, "air", pg.color.THECOLORS["white"], False),
    Block(1, "dirt", pg.color.THECOLORS["saddlebrown"]),
    Block(2, "stone", pg.color.THECOLORS["grey"]),
    Block(3, "wood", pg.color.THECOLORS["brown"]),
    Block(4, "leaves", pg.color.THECOLORS["green"]),
]
