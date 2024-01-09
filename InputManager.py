from enum import Enum

# effbot.org/tkinterbook/tkinter-events-and-bindings.htm

class KEY_STATE(Enum):
    UP = 0,
    DOWN = 1

class KeyboardManager():
    def __init__(self):
        self.keys = {}

    def getState(self, key):
        try:
            return self.keys[key]
        except KeyError as err:
            return KEY_STATE.UP

    def keyDown(self, event):
        self.keys[event.char] = KEY_STATE.DOWN
        print(event.type, " ", event.char)
    def keyUp(self, event):
        self.keys[event.char] = KEY_STATE.UP
        print(event.type, " ", event.char)

class MouseManager():
    def __init__(self):
        self.x = -1
        self.y = -1
        self.btns = {}

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getPos(self):
        return [self.x, self.y]
    def getBtn(self, btn):
        try:
            return self.btns[str(btn)]
        except KeyError as err:
            return KEY_STATE.UP

    def mouseDown(self, event):
        self.x = event.x; self.y = event.y
        self.btns[str(event.num)] = KEY_STATE.DOWN
        #print(event.type, " ", event.num)
    def mouseUp(self, event):
        self.x = event.x; self.y = event.y
        self.btns[str(event.num)] = KEY_STATE.UP
        #print(event.type, " ", event.num)
    def mouseMove(self, event):
        self.x = event.x; self.y = event.y
        #print(event.type, " x", event.x, " y", event.y)

Mouse = MouseManager()
Keyboard = KeyboardManager()
