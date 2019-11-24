import tkinter as tk

class VerticalWall(tk.Frame):
    def __init__(self, parent, have=False):
        tk.Frame.__init__(self, parent)
        self.have = have
        self.canvas = tk.Canvas(self, heigh=25, width=5, highlightthickness=0)
        self.wall = self.canvas.create_rectangle(0, 0, 5, 25, fill="white")
        self.setWall(have)
        self.canvas.pack()

    def setWall(self, have = False):
        self.have = have
        if have == True:
            self.canvas.itemconfig(self.wall, fill="black")
        else:
            self.canvas.itemconfig(self.wall, fill="white")
        self.canvas.update()
        
    def setRedWall(self):
        self.canvas.itemconfig(self.wall, fill="red")
        self.canvas.update()

    def getWall(self):
        return self.have

class HorizontalWall(tk.Frame):
    def __init__(self, parent, have = False):
        tk.Frame.__init__(self, parent)
        self.have = have
        self.canvas = tk.Canvas(self, heigh=5, width=25, highlightthickness=0)
        self.wall = self.canvas.create_rectangle(0, 0, 30, 5, fill="white")
        self.setWall(have)
        self.canvas.pack()

    def setWall(self, have = False):
        self.have = have
        if have == True:
            self.canvas.itemconfig(self.wall, fill="black")
        else:
            self.canvas.itemconfig(self.wall, fill="white")
        self.canvas.update()

    def setRedWall(self):
        self.canvas.itemconfig(self.wall, fill="red")
        self.canvas.update()

    def getWall(self):
        return self.have