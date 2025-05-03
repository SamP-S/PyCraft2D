import pygame as pg

class Entity:
    
    def __init__(self):
        # world position
        self.x = 0
        self.y = 0
        
        # parent tree
        self.parent = None
        self.children = []
        
        # graphics resources
        self.colour = (0, 0, 0, 255)
        self.width, self.height = 1, 1
        self.is_outlined = True
        
    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def update(self, dt):
        pass
    
    def draw(self, surface):
        pass
