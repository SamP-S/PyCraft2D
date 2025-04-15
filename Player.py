import pygame as pg
from math import sin
from Constants import *

class Player:
    
    def __init__(self, name: str):
        self.name = name
        self.x = 0
        self.y = 0
        
    def update(self, dt):
        pass

    def __str__(self):
        return f"{self.name}({self.x}, {self.y})"
