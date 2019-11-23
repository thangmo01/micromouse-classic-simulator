import tkinter as tk
import threading
import serial

from field import Field
from control import RobotControl

serialData = []

class SerialThread(threading.Thread):
    def run(self):
        try:
            ser = serial.Serial('/dev/rfcomm0')
            while True:
                s = ser.readline()
                print(s)
                serialData.append(s)
            ser.close()
        except KeyboardInterrupt:
            exit()

class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.root = parent

        self.field = Field(self, 16, 16)
        self.field.setRobot(15, 0)
        self.field.grid(row=0, column=0)
        
        self.robotControl = RobotControl(self, 
            self.field.robotForward,
            self.field.robotTurnRight, 
            self.field.robotTurnLeft, 
            self.field.robotRun,
            self.field.robotStop
            )
        self.robotControl.grid(row=0, column=1)
        
        self.prevCmd = ""
        # self.updater()

    def update_field(self):
        if len(serialData) != 0:
            if len(serialData) == 1:
                self.prevCmd = serialData[-1]
                self.upByCmd(serialData[-1])
                self.root.update()
            elif len(serialData) > 1 and self.prevCmd != serialData[-1]:
                self.prevCmd = serialData[-1]
                self.upByCmd(serialData[-1])
                self.root.update()
    
    def upByCmd(self, cmd):
        cmd = str(cmd).split(':')
        if cmd[0] == 'vwall' or cmd[0] == 'hwall':
            row = int(cmd[1])
            col = int(cmd[2])
            wall = cmd[3]
            if row < self.field.rowNum and col < self.field.colNum:
                if cmd[0] == 'hwall':
                    print('hwall')
                elif cmd[0] == 'vwall':
                    print('vall')
        else:
            pass 

    def updater(self):
        self.update_field()
        #update every 100 ms
        self.root.after(100, self.updater)

if __name__ == "__main__":
    # SerialThread().start()
    root = tk.Tk()
    root.title("Micromouse Classic")
    root.geometry("800x600")
    App(root).place(x=0, y=0)
    root.mainloop()