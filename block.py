import tkinter as tk

class Block(tk.Frame):
    def __init__(self, parent, row=0, col=0, hwall = True, vwall = True, value = -1):
        self.row = row
        self.col = col
        
        self.value = value
        self.mark = False
        self.flag = False
        self.count = 0

        self.havePass = False
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, heigh=25, width=25, highlightthickness=0)
        self.block = self.canvas.create_rectangle(0, 0, 25, 25, fill="white")
        self.text = self.canvas.create_text(10, 10, text=self.value)
        self.canvas.pack()

    def setPassBlock(self):
        self.havePass = True
        self.canvas.itemconfig(self.block, fill="grey")
    
    def setTargetBlock(self):
        self.canvas.itemconfig(self.block, fill="pink")

    def setValue(self, value):
        self.value = value
        self.canvas.itemconfig(self.text, text=self.value)

    def getBlockInfo(self):
        return {'value': self.value, 'flag': self.flag, 'mark': self.mark, 'count': self.count}
        
    def getValue(self):
        return self.value