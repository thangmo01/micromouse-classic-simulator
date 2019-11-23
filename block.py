import tkinter as tk

class Block(tk.Frame):
    def __init__(self, parent, row=0, col=0, hwall = True, vwall = True):
        self.row = row
        self.col = col
        self.value = 255#16*16
        self.havePass = False
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, heigh=25, width=25, highlightthickness=0)
        #draw block
        self.canvas.create_rectangle(0, 0, 25, 25, fill="white")
        self.canvas.pack()

    def setPassBlock(self):
        self.havePass = True
        self.canvas.create_rectangle(0, 0, 25, 25, fill="grey")
        self.canvas.pack()
        self.canvas.update()
    