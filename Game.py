import StateMachine as SM
from Graphics import *
import time
import Level as LVL
from Physics import *

class GameState(SM.BaseState):

    def enter(self, args):
        self.background = G.createRectangle(0, 0, G.getWidth(), G.getHeight(), fill="blue")
        self.world = LVL.World()
    
    def update(self, dt):
        self.world.update(dt)
        startTime = time.time()
        P.Simulate(self.world, dt)
        #print("sim: ", time.time() - startTime)

    def render(self):
        startTime = time.time()
        player = self.world.children[0] # pull player coords as view translation
        G.viewVec = [-player.x, -player.y]
        G.centreVec = [G.getWidth() / 2, G.getHeight() / 2]
        G.renderRoot(self.world)    # need to change origin to player position as thats the main offset
        #print("draw: ", time.time() - startTime)

class AnimState(SM.BaseState):
    def enter(self, args):
        self.rect = G.createRectangle(200, 200, 100, 100, fill="red")
        print(G.getItemX(self.rect))
        self.dir = 1
        print("entered gameState")
    
    def update(self, dt):
        G.translate(self.rect, 100 * self.dir * dt, 0)
        if G.getItemX(self.rect) < 0:
            self.dir = 1
        elif G.getItemX(self.rect) > 500:
            self.dir = -1
