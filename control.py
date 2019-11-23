import tkinter as tk

class RobotControl(tk.Frame):
    def __init__(self, parent, forward, turnRight, turnLeft, run, stop):
        tk.Frame.__init__(self, parent)
        self.forwardButton = tk.Button(self, text="forward", command=forward)
        self.turnrihtButton = tk.Button(self, text="turnright", command=turnRight)
        self.turnleftButton = tk.Button(self, text="turnleft", command=turnLeft)
        self.runButton = tk.Button(self, text="RUN", command=run)
        self.stopButton = tk.Button(self, text="STOP", command=stop)
        # self.resetButton = tk.Button(self, text="RESET", command=reset)

        self.forwardButton.pack()
        self.turnrihtButton.pack()
        self.turnleftButton.pack()
        self.runButton.pack()
        self.stopButton.pack()
        # self.resetButton.pack()
