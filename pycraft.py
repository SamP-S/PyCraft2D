import tkinter as tk
import StateMachine as SM
import Game
import time
from Graphics import *
import InputManager as Input

# stops key repeating issues caused by os
import os
os.system("xset r off")

class application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.gStateMachine = SM.StateMachine({"gameState": lambda : Game.GameState()})

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="white")
        self.canvas.bind("<ButtonPress>", Input.Mouse.mouseDown)
        self.canvas.bind("<ButtonRelease>", Input.Mouse.mouseUp)
        self.canvas.bind("<Motion>", Input.Mouse.mouseMove)
        self.master.bind("<KeyPress>", Input.Keyboard.keyDown)
        self.master.bind("<KeyRelease>", Input.Keyboard.keyUp)
        self.canvas.pack(side="bottom")

    def main(self):
        global exit_flag
        G.setCanvas(self.canvas)
        self.gStateMachine.change("gameState")
        startTime = time.time()
        while exit_flag == False:
            self.update_idletasks()
            self.update()
            dt = time.time() - startTime
            startTime = time.time()
            self.gStateMachine.update(dt)
            if exit_flag == False:
                self.gStateMachine.render()
            #print("frametime = ", time.time() - startTime)

    def on_quit(self):
        global exit_flag
        exit_flag = True
        self.master.destroy()


def main():
    global exit_flag
    exit_flag = False
    root = tk.Tk()
    app = application(master=root)
    app.master.protocol("WM_DELETE_WINDOW", app.on_quit)
    app.main()

if __name__ == "__main__":
    print("main pycraft")
    main()
else:
    print("import pycraft")


# reset os settings back to normal
os.system("xset r on")