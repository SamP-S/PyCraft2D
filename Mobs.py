import InputManager as Input
from Base import GameObject, F_TYPE
from enum import Enum
from Physics import *
from Graphics import *

SPEED = 100
JUMP = 400

# USE FOR MOB CONTROLLERS/AI
class M_TYPE(Enum):
    PLAYER = 0
    COW = 1
    ZOMBIE = 2

class Player(GameObject):
    def __init__(self, parent, x, y):
        super().__init__(parent, x, y)
        self.height = 2
        self.inventory = None
        self.hotbar = []
        self.AddComponent(Rigidbody(self, mass=100))
        self.AddComponent(RectCollider(self, 0.5, 1, 1, 2))
        self.AddComponent(RectGraphic(self, 0, 0, 1, 2, fill="blue"))
        
    # WILL NEED UPDATING TO PHYSICS SYSTEM
    # BASIC ASS FOR NOW
    def update(self, dt):
        rb = self.GetComponent(Rigidbody)
        xDir, yDir = 0, 0
        # Horizontal movement
        if Input.Keyboard.getState("d") == Input.KEY_STATE.DOWN:
            xDir += 1
        elif Input.Keyboard.getState("a") == Input.KEY_STATE.DOWN:
            xDir -= 1
        # Vertical movement
        if Input.Keyboard.getState("w") == Input.KEY_STATE.DOWN:
            yDir += 1
        elif Input.Keyboard.getState("s") == Input.KEY_STATE.DOWN:
            pass
        # movement validation done inside the physics engine using dx and dy
        rb.AddForce(xDir * SPEED * rb.mass, yDir * JUMP * rb.mass, F_TYPE.ACCELERATION)