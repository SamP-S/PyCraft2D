class BaseState():
    def __init__(self):
        pass
    def enter(self, args=None):
        pass
    def exit(self):
        pass
    def update(self, dt):
        pass
    def render(self):
        pass

class ExampleState(BaseState):
    def __init__(self):
        print("example state instantiated")
        self.x = 10
    def enter(self, args):
        print("example name = ", args["name"])
    def exit(self):
        print("bye bye")
    def update(self, dt):
        #print("delta time = ", dt, "s")
        pass
    def render(self):
        #print("draw if draw")
        pass


class StateMachine():

    def __init__(self, states=None):
        self.empty = BaseState()
        if states != None:
            self.states = states
        else:
            self.states = {}
        self.current = self.empty

    def change(self, stateName, enterArgs={}):
        if stateName in self.states.keys():
            self.current.exit()
            self.current = self.states[stateName]()
            self.current.enter(enterArgs)

    def update(self, dt):
        self.current.update(dt)
    
    def render(self):
        self.current.render()