from enum import Enum
import Mobs
from Base import GameObject
from Graphics import *
from Physics import *

# threading 
#import threading
#import logging

class GEN_TYPE(Enum):
    FLAT = 0
    SIMPLE_RANDOM = 1

class BLOCK(Enum):
    AIR = 0
    DIRT = 1
    STONE = 2
    BEDROCK = 3
    LOG = 4
    LEAF = 5
    WOOD = 6
    GRASS = 7
    IRON = 8
    GOLD = 9
    DIAMOND = 10

BLOCK_COLOUR = [
    "lightskyblue", # air
    "salmon4", # dirt
    "gray40", # stone
    "gray15", # bedrock
    "saddle brown", # log
    "forest green", # leaf
    "tan1", # wood
    "lawn green", # grass
    "snow2", # iron
    "gold", # gold
    "cyan" # diamond
]

class ChangeLog:
    def __init__(self, x, y, bID):
        self.x = x
        self.y = y
        self.bID = bID

class ChangeBuffer:
    def __init__(self, x):
        self.x = x
        self.buffer = []

def flatWorldPillar(x=0):
    """ Returns list of block_ids for the pillar at given x
        0 = bedrock
        1 - 59 = stone
        60 - 63 = dirt
        64 - 255 = air """
    blocks = [0] * 256
    blocks[0] = BLOCK.BEDROCK
    for i in range(1, 60):
        blocks[i] = BLOCK.STONE
    for i in range(60, 63):
        blocks[i] = BLOCK.DIRT
    blocks[63] = BLOCK.GRASS
    for i in range(64, 256):
        blocks[i] = BLOCK.AIR
    return blocks

def flatWorldBlock(x=0):
    blocks = []
    for i in range(16):
        blocks.append(flatWorldPillar(x + i))
    return blocks

"""
class Pillar(GameObject):
    def __init__(self, parent, x, sub_buf=None, blockGen=flatWorldPillar):
        super().__init__(parent, x, 0)
        self.blockIDs = blockGen(x + parent.seed)
        if sub_buf == None:
            sub_buf = ChangeBuffer(x)
        self.loadBuffer(sub_buf)
        self.genRects()

    def loadBuffer(self, sub_buf):
        self.sub_buf = sub_buf
        for sub in sub_buf.buffer:
            self.blockIDs[sub.y] = sub.bID

    def genRects(self):
        for i in range(len(self.components) - 1, 0, -1):
            if self.components[i].type != None:
                gID = self.components.pop(i)
                G.deleteObject(gID)
        for i in range(256):
            if self.blockIDs[i] != BLOCK.AIR:
                colour = BLOCK_COLOUR[self.blockIDs[i].value]
                self.AddComponent(RectGraphic(self, 0, i, 1, 1, fill=colour))
                self.AddComponent(RectCollider(self, 0.5, 0.5 + i, 1, 1))
        #print(self.components)
"""

def chunkLoadCollider(parent):
    triggerCollider = RectCollider(parent, 8, 128, 16, 256, True)
    #triggerCollider.OnTriggerEnter = lambda self, collider: (triggerCollider.gameObject.parent.checkChunksFlag := [True, triggerCollider.gameObject.x])
    return triggerCollider

class Block(GameObject):
    def __init__(self, parent, x=0, sub_buf=None, blockGen=flatWorldBlock):
        super().__init__(parent, x, 0)
        self.blockIDs = blockGen(x + parent.seed)
        if sub_buf == None:
            sub_buf = ChangeBuffer(x)
        self.loadBuffer(sub_buf)
        self.generate()

    def loadBuffer(self, sub_buf):
        self.sub_buf = sub_buf
        for sub in sub_buf.buffer:
            self.blockIDs[sub.y] = sub.bID

    def generate(self):
        self.components.clear()
        self.AddComponent(chunkLoadCollider(self))
        for i in range(16):
            for j in range(256):
                if self.blockIDs[i][j] != BLOCK.AIR:
                    colour = BLOCK_COLOUR[self.blockIDs[i][j].value]
                    self.AddComponent(RectGraphic(self, i, j, 1, 1, fill=colour))
                    self.AddComponent(RectCollider(self, 0.5 + i, 0.5 + j, 1, 1))
        print("completed block", self.x, " generation")

class Level(GameObject):
    def __init__(self, parent, seed, x=0, y=0):
        super().__init__(parent, x, y)
        self.seed = seed
        self.offBuffer = [] # "offscreen buffer" = all buffers of pillars that are not currently loaded
        self.loadFile("agh")
        self.checkChunksFlag = [False, 0]
        
    def update(self, dt):
        if self.checkChunksFlag[0]:
            self.checkChunks(self.checkChunksFlag[1])
        for child in self.children:
            child.update(dt)

    def loadFile(self, filePath):
        # parse out seed and generation information
        self.seed = 0
        self.genType = flatWorldBlock
        # fill change buffer from file then load pillars
        for i in range (-1, 2):    
            sub_buf = ChangeBuffer(i * 16)
            #thread = threading.Thread(target=self.loadPillar, args=[i], daemon=True)  #daemon mean main dont care
            #thread.start()
            self.loadBlock(i * 16, self.genType, sub_buf)
        print("level loaded")
    
    def saveFile(self, filePath):
        # unload all pillars then save change buffer to file
        pass

    def checkChunks(self, x):
        # check player distance to pillars to check if load / unload needed
        index = 0
        numChildren = len(self.children)
        for i in range(numChildren):
            if self.children[i].x == x:
                index = i
        numLeft = index
        numRight = numChildren - index - 1
        ##### NEED TO ADD SUBSTITUTION BUFFERS HERE #####
        # add block left
        if numLeft < 2:
            x = self.children[0].x - 16
            self.children = [Block(self, x)] + self.children
        # add block right
        elif numRight < 2:
            x = self.children[numChildren - 1].x + 16
            self.children = [Block(self, x)] + self.children
        # pop block left
        elif numLeft > 3:
            self.children.pop(0)
        # pop block right
        elif numRight > 3:
            self.children.pop(numChildren - 1)

    def loadBlock(self, x, genType, sub_buf):
        # must gen pillar and use off buffer to recreate changes
        self.AddChild(Block(self, x, sub_buf, genType))
"""
    def unloadBlock(self, x):
        # must move change buffer to the off buffer
        for child in self.children:
            if child.x == x:
                self.offBuffer.append(child.changes)
                self.RemoveChild(child)
"""

class World(GameObject):
    def __init__(self, seed=0, genType=GEN_TYPE.FLAT):
        super().__init__(None)
        self.seed = seed
        self.genType = genType
        self.children.append(Mobs.Player(self, 0, 64))
        self.children.append(Level(self, seed=seed))
        
    def update(self, dt):
        for child in self.children:
            child.update(dt)
