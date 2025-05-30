from __future__ import annotations
import pygame as pg

class Entity:
    
    def __init__(self):
        # world position
        self.x:float = 0.0
        self.y:float = 0.0
        
        # parent tree
        self.parent:Entity|None = None
        self.children:list[Entity] = []
        
    def add_child(self, child:Entity):
        """Add a child entity to this entity."""
        assert(isinstance(child, Entity))
        self.children.append(child)
        child.parent = self

    def update(self, dt:float):
        """Update this entity over time."""
        pass
    
    def draw(self, layer:pg.Surface):
        """Draw this entity."""
        assert(layer is not None)
        