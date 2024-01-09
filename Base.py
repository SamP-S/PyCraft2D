from enum import Enum

class COMP_TYPE(Enum):
    NONE = 0
    # PHYSICS
    PHYSICS = 1
    COLLIDER = 2
    RECT_COLLIDER = 3
    CIRCLE_COLLIDER = 4  # potentially add later but not right now
    RIGIDBODY = 5
    # GRAPHICS
    GRAPHICS = 6
    ARC = 7
    OVAL = 8
    RECTANGLE = 9
    LINE = 10
    POLYGON = 11
    BITMAP = 12
    IMAGE = 13
    TEXT = 14
    WINDOW = 15

class GameObject:
    def __init__(self, parent, x=0, y=0):
        self.parent = parent
        self.x, self.y = x, y
        self.children = []
        self.components = []

    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def AddComponent(self, component):
        if type(component) == Rigidbody:
            if self.GetComponent(Rigidbody) != None:
                return False
            colliders = self.GetComponents(RectCollider)
            if colliders != None:
                for collider in colliders:
                    collider.attachedRigidbody = component
        elif type(component) == RectCollider:
            rb = self.GetComponent(Rigidbody)
            if rb != None:
                component.attachedRigidbody = rb
        self.components.append(component)
        return True
    def RemoveComponent(self, component):
        self.components.remove(component)
        return True

    def AddChild(self, child):
        self.children.append(child)
    def RemoveChild(self, child):
        self.children.remove(child)

    def GetComponent(self, compType):
        """ Returns first component of given type
            else returns None if none found """
        for comp in self.components:
            if type(comp) == compType:
                return comp
            return None

    def GetComponents(self, compType):
        """ Returns all components of given type
            Returns None if no components found """
        comps = []
        for comp in self.components:
            if type(comp) == compType:
                comps.append(comp)

        if len(comps) == 0:
            return None
        else:
            return comps

    def GetComponentsInParent(self, compType):
        if self.parent == None:
            return None
        return self.parent.GetComponents(compType)
    
    def GetComponentsInChildren(self, compType):
        if len(self.children) == 0:
            return None
        comps = []
        for child in self.children:
            childComps =  child.GetComponents(compType)
            if childComps != None:
                comps += childComps
        if len(comps) == 0:
            return None
        else:
            return comps

class Component:
    def __init__(self, gameObject):
        self.gameObject = gameObject
        self.type = COMP_TYPE.NONE


### GRAPHICS ###
class GraphicsComponent(Component):
    def __init__(self, gameObject, gID, x=0, y=0):
        super().__init__(gameObject)
        self.x = x
        self.y = y
        self.gID = gID
        self.type = COMP_TYPE.GRAPHICS


### PHYSICS ###

### BASE ###
class PhysicsComponent(Component):
    def __init__(self, gameObject):
        super().__init__(gameObject)
        self.type = COMP_TYPE.NONE

### RIGIDBODY ###
class F_TYPE(Enum):
    ACCELERATION = 0
    IMPULSE = 1
    VELOCITY = 2

def sign(a):
    if a < 0:
        return -1
    else:
        return 1

class Rigidbody(PhysicsComponent):
    def __init__(self, gameObject, mass=2, drag=0.3, maxVel=5, maxAcc = 50):
        super().__init__(gameObject)
        self.type = COMP_TYPE.RIGIDBODY
        self.mass = mass
        self.vX, self.vY = 0, 0
        self.aX, self.aY = 0, 0
        self.drag = drag
        self.maxAcc = maxAcc
        self.maxVel = maxVel
        self.forceX = 0
        self.forceY = 0
        self.momentumX = 0
        self.momentumY = 0
        
    def AddForce(self, fX, fY, fType = F_TYPE.ACCELERATION):
        self.forceX += fX
        self.forceY += fY

    def update(self, dt):
        self.AddForce(0, self.mass * -9.8)
        self.AddForce(self.drag * -self.vX * self.mass, self.drag * -self.vY * self.mass)
        accX, accY = self.forceX / self.mass, self.forceY / self.mass
        # force = mass * acceleration
        self.aX = min(abs(accX), self.maxAcc) * sign(accX)
        self.aY = min(abs(accY), self.maxAcc) * sign(accY)
        velY = self.vY
        # velocity = v0 + acceleration * time
        speedX = self.vX + self.aX * dt
        speedY = self.vY + self.aY * dt
        if self.vY < speedY:
            print("NO NO")
        self.vX = min(abs(speedX), self.maxVel) * sign(speedX) 
        self.vY = min(abs(speedY), self.maxVel) * sign(speedY)
        self.vX = self.vX #* self.drag
        self.vY = self.vY #* self.drag
        # apply velocity
        #self.gameObject.x += self.vX * dt
        #self.gameObject.y += self.vY * dt
        print("ACC: x=", self.aX, " y=", self.aY)
        print("VEL: x=", self.vX, " y=", self.vY)
        self.momentumX = self.mass * self.vX
        self.momentumY = self.mass * self.vY
        self.forceX, self.forceY = 0,0


### COLLIDERS ###
class Collider(PhysicsComponent):
    def __init__(self, gameObject, isTrigger=False, enabled=True):
        super().__init__(gameObject)
        self.type = COMP_TYPE.COLLIDER
        self.isTrigger = isTrigger
        self.enabled = enabled
        self.attachedRigidbody = None

    # cartesian coordinate functions for sweep & prune
    def getMinX(self):
        return 0
    def getMaxX(self):
        return 0
    def getMinY(self):
        return 0
    def getMaxY(self):
        return 0
    def getOrigin(self):
        origin = [self.gameObject.x, self.gameObject.y]
        obj = self.gameObject
        while obj.parent != None:
            obj = obj.parent
            origin[0] += obj.x
            origin[1] += obj.y
        return origin

    def getBroadMinX(self):
        return 0
    def getBroadMaxX(self):
        return 0
    def getBroadMinY(self):
        return 0
    def getBroadMaxY(self):
        return 0

    # collision callback event handlers
    def OnCollisionEnter(self, collision):
        pass
    def OnCollisionStay(self, collision):
        pass
    def OnCollisionExit(self, collision):
        pass
    def OnTriggerEnter(self, collider):
        pass
    def OnTriggerStay(self, collider):
        pass
    def OnTriggerExit(self, collider):
        pass


class RectCollider(Collider):
    """  """
    def __init__(self, gameObject, cX=0, cY=0, sX=1, sY=1, isTrigger=False, enabled=True, rigidbody=None):
        super().__init__(gameObject, isTrigger, enabled)
        self.type = COMP_TYPE.RECT_COLLIDER
        self.cX, self.cY = cX, cY
        self.sX, self.sY = sX, sY

    # narrowphase min/max positions
    def getMinX(self):
        return self.getOrigin()[0] + self.cX - self.sX / 2
    def getMaxX(self):
        return self.getOrigin()[0] + self.cX + self.sX / 2
    def getMinY(self):
        return self.getOrigin()[1] + self.cY - self.sY / 2
    def getMaxY(self):
        return self.getOrigin()[1] + self.cY + self.sY / 2
        
    # broadphase min/max positions
    def getBroadMinX(self):
        if self.attachedRigidbody == None:
            return self.getMinX()
        return self.getOrigin()[0] - abs(self.attachedRigidbody.vX) + self.cX - self.sX / 2
    def getBroadMaxX(self):
        if self.attachedRigidbody == None:
            return self.getMinX()
        return self.getOrigin()[0] + abs(self.attachedRigidbody.vX) + self.cX + self.sX / 2
    def getBroadMinY(self):
        if self.attachedRigidbody == None:
            return self.getMinX()
        return self.getOrigin()[1] - abs(self.attachedRigidbody.vY) + self.cY - self.sY / 2
    def getBroadMaxY(self):
        if self.attachedRigidbody == None:
            return self.getMinX()
        return self.getOrigin()[1] + abs(self.attachedRigidbody.vY) + self.cY + self.sY / 2