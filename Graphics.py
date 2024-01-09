from Base import GraphicsComponent, COMP_TYPE
from enum import Enum

import time

# POLY OBJECTS:
# Draws lines from a list of points
# Line = open; Poly = closed

# BOX OBJECTS:
# Draws object by reference of a boundary box
# arc, oval, rectangle

# POSITIONAL OBJECTS:
# Draws objects in reference to a cartesian point
# bitmap, image, text, window

# OBJECT PRIORITY:
# RECTANGLE & TEXT
# IMAGE

# * NOTE * from Base import Component, COMP_TYPE
# Window can be used to store widgets on top of canvas

# ** NOTE **
# All graphics are drawn from the top left corner BUT all physics is calculated from the bottom left

class RectGraphic(GraphicsComponent):
    def __init__(self, gameObject, x, y, w, h, **options):
        gID = G.createRectangle(x, y, w, h, **options)
        super().__init__(gameObject, gID, x, y)
        self.w, self.h = w, h
        self.type = COMP_TYPE.RECTANGLE

class GraphicsEngine():
    PUR = 800 / 20 # PIXEL TO UNIT RATION (float)
    
    def __init__(self):
        self.canvas = None
        self.hasSurface = False
        self.viewVec = [0, 0]
        self.centreVec = [0, 0]

    """
    def createPolyObject(self, type, coords, options):
        if type == "LINE":
            pass    #create_line(coords, **options)
        elif type == "POLYGON":
            pass    #create_polygon(coords, **options)
        else:
            print("ERROR: Invalid graphics object type")
            return -1
    """
    
    def getWidth(self):
        if self.canvas == None:
            return -1
        return self.canvas.winfo_width()
    
    def getHeight(self):
        if self.canvas == None:
            return -1
        return self.canvas.winfo_height()

    # item methods
    def getItemX(self, id):
        #print("getItemX ", id)
        return self.canvas.coords(id)[0]
    def getItemY(self, id):
        return self.canvas.coords(id)[1]
    def setItemBBox(self, id, x, y, w, h):
        canvHeight = self.getHeight()
        coords = [  
                                    ((x + self.viewVec[0]) * self.PUR + self.centreVec[0]), 
                    canvHeight -    ((y + self.viewVec[1]) * self.PUR + self.centreVec[1]), 
                                    ((x + w + self.viewVec[0]) * self.PUR + self.centreVec[0]),  
                    canvHeight -    ((y + h + self.viewVec[1]) * self.PUR + self.centreVec[1])
                ]
        # -y is used to invert drawing origin from top left to bottom left
        # this allows for the game, physics and graphics origin to all align
        self.canvas.coords(id, coords[0], coords[1], coords[2], coords[3])

    # transformations
    def translate(self, id, dx, dy):
        self.canvas.move(id, dx, dy)
        #print("translate item", id, " x", dx, "y", dy)
    def scale(self, id, sx, sy):
        pos = [self.getItemX(id), self.getItemY(id)]
        print("pos=",pos)
        self.canvas.scale(id, sx, sy, pos[0], pos[1])
        pass
    def rot(self, id, rz):
        pass

    def createRectangle(self, x, y, w, h, **options):
        return self.canvas.create_rectangle(x,y,w,h, options)
    def deleteObject(self, gID):
        self.canvas.delete(gID)

    def setCanvas(self, canvas):
        self.canvas = canvas

    def renderNode(self, gameObj, parentOrigin):
        localOrigin = [gameObj.x - parentOrigin[0], gameObj.y - parentOrigin[1]]
        for comp in gameObj.components:
            #startTime = time.time()
            if type(comp) == RectGraphic:
                if comp.gID >= 0:
                    bbox = [    (comp.x + localOrigin[0]),
                                (comp.y + localOrigin[1]),
                                (comp.w),
                                (comp.h)    ]
                    G.setItemBBox(comp.gID, bbox[0], bbox[1], bbox[2], bbox[3])
                    #self.canvas.update()
            #print("rect draw: ", time.time() - startTime)
        for child in gameObj.children:
            self.renderNode(child, localOrigin)

    def renderRoot(self, world):
        for child in world.children:
            self.renderNode(child, [0, 0])


G = GraphicsEngine()