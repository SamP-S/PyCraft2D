from Base import RectCollider, Rigidbody
from enum import Enum
import time

class COLLISION_TYPE(Enum):
    STATICS = 0
    RIGIDSTATIC = 1
    RIGIDS = 2

### COLLISIONS ###
# FLESH OUT COLLISION INFORMATION
# Colliders hit
# game object hit
# rigid body hit
class Collision:

    def __init__(self, colType, isTrigger, colliderA, colliderB, normalX, normalY, xEntryTime, yEntryTime, xExitTime, yExitTime):
        self.type = colType
        self.isTrigger = isTrigger
        self.cA = colliderA
        self.cB = colliderB
        self.normalX = normalX
        self.normalY = normalY
        self.xEntryTime = xEntryTime
        self.yEntryTime = yEntryTime
        self.xExitTime = xExitTime
        self.yExitTime = yExitTime

    def __eq__(self, other):
        eqFirst, eqSecond, eqFirstOp, eqSecondOp = False, False, False, False
        if other == None:
            return False
        if self.cA == other.cA:         eqFirst = True
        if self.cB == other.cB:         eqSecond = True
        if self.cA == other.cB:         eqFirstOp = True
        if self.cB == other.cA:         eqSecondOp = True
        return (eqFirst and eqSecond) or (eqFirstOp and eqSecondOp)
    
    def getEntryTime(self):
        return min(self.xEntryTime, self.yEntryTime)
    def getExitTime(self):
        return max(self.xExitTime, self.yExitTime)

### ENGINE ###
class PhysicsEngine:
    def __init__(self):
        self.gravity = 9.8
        self.axisLst = []
        self.sweepPairs = []
        self.cur_collisions = []
        self.next_collisions = []
        self.rigidbodies = []

    def castFineRay(self, start, dir, dist, callback):
        pass
    def castInfRay(self, start, dir, callback):
        """ Stops at first object it collides with """
        pass

#####################################################################################
## Collision Detection ##
    def aabbCheck(self, a, b):
        isX, isY = False, False
        if a.getMinX < b.getMaxX() and a.getMaxX > b.getMinX():
            isX = True
        if a.getMinY < b.getMaxY() and a.getMaxY > b.getMinY():
            isY = True
        return (isX and isY)
    
    def checkRigidStaticAABB(self, colliderR, colliderS):
        """ Checks collision between moving object (has ridigbody) and
            static object (no rigidbody)
            Returns collision object
        """
        rb = colliderR.attachedRigidbody
        vX = rb.vX
        vY = rb.vY
        xEntry, xExit = 0, 0
        yEntry, yExit = 0, 0
        
        # check x-axis entry and exit points
        if vX > 0:
            xEntry = colliderS.getMinX() - colliderR.getMaxX()
            xExit = colliderS.getMaxX() - colliderR.getMinX()
        else:
            xEntry = colliderS.getMaxX() - colliderR.getMinX()
            xExit = colliderS.getMinX() - colliderR.getMaxX()
        # check y-axis entry and exit points
        if vY > 0:
            yEntry = colliderS.getMinY() - colliderR.getMaxY()
            yExit = colliderS.getMaxY() - colliderR.getMinY()
        else:
            yEntry = colliderS.getMaxY() - colliderR.getMinY()
            yExit = colliderS.getMinY() - colliderR.getMaxY()
        
        xEntryTime, xExitTime = 0, 0
        yEntryTime, yExitTime = 0, 0
        # calculate time of entry/exit on x-axis
        if vX == 0:
            xEntryTime, xExitTime = float("-inf"), float("inf")
        else:
            xEntryTime, xExitTime = xEntry / vX, xExit / vX
        # calculate time of entry/exit on y-axis
        if vY == 0:
            yEntryTime, yExitTime = float("-inf"), float("inf")
        else:
            yEntryTime, yExitTime = yEntry / vY, yExit / vY
        
        entryTime = max(xEntryTime, yEntryTime)
        exitTime = min(xExitTime, yExitTime)

        # no collision
        if entryTime > exitTime or (xEntryTime < 0 and yEntryTime < 0) or xEntryTime > 1 or yEntryTime > 1:
            return None
        # yes collision
        else:
            if xEntryTime > yEntryTime:
                if xEntry < 0:
                    normalX, normalY = 1, 0
                else:
                    normalX, normalY = -1, 0
            else:
                if yEntry < 0:
                    normalX, normalY = 0, 1
                else:
                    normalX, normalY = 0, -1
        colType = COLLISION_TYPE.RIGIDSTATIC
        isTrigger = colliderR.isTrigger or colliderS.isTrigger
        return Collision(colType, isTrigger, colliderR, colliderS, normalX, normalY, xEntryTime, yEntryTime, xExitTime, yExitTime)

#####################################################################################
## Tree Traversal ##
    def parseNodeRigidbodies(self, node, dt):
        rb = node.GetComponent(Rigidbody)
        if rb != None:
            self.rigidbodies.append(rb)
            rb.update(dt)
        for child in node.children:
            self.parseNodeRigidbodies(child, dt)
    
    def parseNodeColliders(self, gameObj):
        comps = gameObj.GetComponents(RectCollider)
        if comps != None:
            self.axisLst += comps
        for child in gameObj.children:
            self.parseNodeColliders(child)

####################################################################################
    
    def sortAxisList(self):
        # uses insert sort which is not optimal for first sort
        # but is much faster on a frame by frame basis
        for i in range(1, len(self.axisLst)):
            j = i
            while j > 0 and self.axisLst[j-1].getBroadMinX() > self.axisLst[j].getBroadMinX():
                tmp = self.axisLst[j-1]
                self.axisLst[j-1] = self.axisLst[j]
                self.axisLst[j] = tmp

    def sweepAndPrune(self):
        # assumes the axis list is already sorted
        activeLst = []
        self.next_collisions = []
        count = 0
        for item in self.axisLst:
            if count == 1026:
                print("1026")
            if len(activeLst) > 0:
                x = item.getBroadMinX()
                for test in activeLst:
                    tX = test.getBroadMaxX()
                    if tX <= x:
                        activeLst.remove(test)
                    else:
                        if test.gameObject != item.gameObject:
                            # do narrow phase testing directly from broadphase
                            rbTest = test.attachedRigidbody
                            rbItem = item.attachedRigidbody
                            collision = None
                            if rbTest == None and rbItem == None:
                                print("static on static")
                            elif rbTest != None and rbItem == None:
                                collision = self.checkRigidStaticAABB(test, item)
                            elif rbTest == None and rbItem != None:
                                collision = self.checkRigidStaticAABB(item, test)
                            else:
                                # add rigid on rigid collisions
                                print("rigid on rigid")
                            # add collision to list
                            if collision != None:
                                self.next_collisions.append(collision)
            activeLst.append(item)
            count += 1
        
    def collisionResponse(self, dt):
        rigidTimes = [[dt, dt]] * len(self.rigidbodies)
        for collision in self.next_collisions:
            #NEED TO ADD ONCOLLISION CALLS FOR ALL SCENARIOS
                if collision.isTrigger:
                    if collision.cA.isTrigger:
                        collision.cA.OnTriggerEnter(collision.cB)
                    if collision.cB.isTrigger:
                        collision.cB.OnTriggerEnter(collision.cA)
                    continue

                # add handle for each collision type
                if collision.type == COLLISION_TYPE.STATICS:
                    pass
                elif collision.type == COLLISION_TYPE.RIGIDSTATIC:
                    rigidTime = rigidTimes[self.rigidbodies.index(collision.cA.attachedRigidbody)]
                    minX = rigidTime[0]
                    minY = rigidTime[1]
                    if collision.xEntryTime < minX and collision.xEntryTime >= 0 and collision.normalX != 0:
                        rigidTime[0] = collision.xEntryTime
                    if collision.yEntryTime < minY and collision.yEntryTime >= 0 and collision.normalY != 0:
                        rigidTime[1] = collision.yEntryTime
                elif collision.type == COLLISION_TYPE.RIGIDS:
                    pass
        # step rigids with their collision time limits applied
        for i in range(len(rigidTimes)):
            rb = self.rigidbodies[i]
            gameObject = rb.gameObject
            maxTimeX, maxTimeY = rigidTimes[i]
            gameObject.x += maxTimeX * rb.vX
            gameObject.y += maxTimeY * rb.vY          


####################################################################################
## Engine Simulation Update ##
    def Simulate(self, world, dt):
        startTime = time.time()
        self.rigidbodies = []
        self.parseNodeRigidbodies(world, dt)
        #print("parse rigid = ", time.time() - startTime)
        self.axisLst = []
        self.parseNodeColliders(world)
        self.sortAxisList()
        #print("parse colliders = ", time.time() - startTime)
        self.sweepAndPrune()
        #print("weep and sweep = ", time.time() - startTime)
        self.collisionResponse(dt)

P = PhysicsEngine()