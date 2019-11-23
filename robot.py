import tkinter as tk

class Robot(tk.Frame):
    def __init__(self, parent, py=0, px=0):
        tk.Frame.__init__(self, parent)
        self.direction = 'N'
        self.py = py
        self.px = px
        self.canvas = tk.Canvas(self, heigh=25, width=25, highlightthickness=0)
        self.drawRobot()

    def getDirection(self):
        return self.direction

    def drawRobot(self):
        if self.direction == 'N':
            self.canvas.delete('all')
            self.canvas.create_rectangle(5, 5, 20, 20, fill="red")
            self.canvas.create_rectangle(5, 5, 20, 8, fill="yellow")
            # self.canvas.create_rectangle(2, 5, 5, 20, fill="black")
            # self.canvas.create_rectangle(20, 5, 23, 20, fill="black")
            self.canvas.pack()

        elif self.direction == 'E':
            self.canvas.delete('all')
            self.canvas.create_rectangle(5, 5, 20, 20, fill="red")
            self.canvas.create_rectangle(17, 5, 20, 20, fill="yellow")
            self.canvas.pack()

        elif self.direction == 'S':
            self.canvas.delete('all')
            self.canvas.create_rectangle(5, 5, 20, 20, fill="red")
            self.canvas.create_rectangle(5, 17, 20, 20, fill="yellow")
            self.canvas.pack()

        elif self.direction == 'W':
            self.canvas.delete('all')
            self.canvas.create_rectangle(5, 5, 20, 20, fill="red")
            self.canvas.create_rectangle(5, 5, 8, 20, fill="yellow")
            self.canvas.pack()

        self.canvas.update()

    def forward(self):
        if self.direction == 'N':
            self.py -= 1
        elif self.direction == 'E':
            self.px += 1
        elif self.direction == 'S':
            self.py += 1
        else:
            self.px -= 1

    def turnRight(self):
        if self.direction == 'N':
            self.direction = 'E'
        elif self.direction == 'E':
            self.direction = 'S'
        elif self.direction == 'S':
            self.direction = 'W'
        else:
            self.direction = 'N'
        self.drawRobot()

    def turnLeft(self):
        if self.direction == 'N':
            self.direction = 'W'
        elif self.direction == 'E':
            self.direction = 'N'
        elif self.direction == 'S':
            self.direction = 'E'
        else:
            self.direction = 'S'
        self.drawRobot()

    def setPosition(self, py, px):
        self.py = py
        self.px = px

    def getPosition(self):
        return self.py, self.px
