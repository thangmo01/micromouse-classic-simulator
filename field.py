import tkinter as tk
import time

from robot import Robot
from wall import VerticalWall, HorizontalWall
from block import Block

class Field(tk.Frame):
    def __init__(self, parent, rowNum = 16, colNum = 16):
        tk.Frame.__init__(self, parent)
        self.runRobotStat = False
        self.rowNum = rowNum
        self.colNum = colNum

        self.robot = Robot(self)

        #create empty blocks
        self.blocks = [None] * rowNum
        for i in range(rowNum):
            self.blocks[i] = [None] * colNum
        
        #create empty vwalls
        self.vwalls = [None] * rowNum
        for i in range(rowNum):
            self.vwalls[i] = [None] * (colNum+1)

        #create empty hwalls
        self.hwalls = [None] * (rowNum+1)
        for i in range(rowNum+1):
            self.hwalls[i] = [None] * colNum

        self.setField()

    def setField(self):
        #set blocks
        for r in range(self.rowNum):
            for c in range(self.colNum):
                self.vwalls[r][c] = VerticalWall(self)
                self.vwalls[r][c].grid(row=r*2 + 1, column=c*2)
                self.hwalls[r][c] = HorizontalWall(self)
                self.hwalls[r][c].grid(row=r*2, column=c*2 + 1)
                self.blocks[r][c] = Block(self, row=r*2 + 1, col=c*2 + 1);
                self.blocks[r][c].grid(row=r*2 + 1, column=c*2 + 1)

        for i in range(self.rowNum):
            self.vwalls[i][self.colNum] = VerticalWall(self)
            self.vwalls[i][self.colNum].grid(row=i*2 + 1, column=(self.colNum+1) * 2)

        for i in range(self.colNum):
            self.hwalls[self.rowNum][i] = HorizontalWall(self)
            self.hwalls[self.rowNum][i].grid(row=(self.rowNum+1) * 2, column=i*2 + 1)

        from map import maps
        hwalls = maps['2018']['hwalls']
        vwalls = maps['2018']['vwalls']

        i = 0
        for hwall in hwalls:
            for h in hwall:
                self.hwalls[i][h].setWall(True)
            i += 1

        i = 0
        for vwall in vwalls:
            for v in vwall:
                self.vwalls[i][v].setWall(True)
            i += 1

    def setRobot(self, py, px):
        self.robot.setPosition(py, px)
        self.blocks[py][px].grid_remove()
        self.robot.grid(row=py*2 + 1, column=px*2 + 1)
        self.robot.canvas.update()

    def robotCanMove(self):
        py, px = self.robot.getPosition()
        d = self.robot.getDirection()

        return (d == 'N' and py - 1 >= 0) or (d == 'E' and px + 1 < self.colNum) or (d == 'W' and px - 1 >= 0) or (d == 'S' and py + 1 < self.rowNum)

    def robotForward(self):
        if self.robotCanMove() == True:
            py, px = self.robot.getPosition()
            self.blocks[py][px].grid(row=py*2 + 1, column=px*2 + 1)
            self.blocks[py][px].setPassBlock()
            self.robot.grid_remove()

            self.robot.forward()
            py, px = self.robot.getPosition()
            self.blocks[py][px].grid_remove()
            self.robot.grid(row=py*2 + 1, column=px*2 + 1)
            self.robot.canvas.update()

    def robotTurnRight(self):
        self.robot.turnRight()

    def robotTurnLeft(self):
        self.robot.turnLeft()

    def robotGetState(self):
        py, px = self.robot.getPosition()
        state = 0
        d = self.robot.getDirection()
        if d == 'N':
            if self.vwalls[py][px].have == True:
                state += 1
            if self.hwalls[py][px].have == True:
                state += 2
            if self.vwalls[py][px + 1].have == True:
                state += 4
        elif d == 'E':
            if self.hwalls[py][px].have == True:
                state += 1
            if self.vwalls[py][px + 1].have == True:
                state += 2
            if self.hwalls[py + 1][px].have == True:
                state += 4
        elif d == 'S':
            if self.vwalls[py][px + 1].have == True:
                state += 1
            if self.hwalls[py + 1][px].have == True:
                state += 2
            if self.vwalls[py][px].have == True:
                state += 4
        else:
            if self.hwalls[py + 1][px].have == True:
                state += 1
            if self.vwalls[py][px].have == True:
                state += 2
            if self.hwalls[py][px].have == True:
                state += 4

        return state

    def robotRun(self):
        self.runRobotStat = True
        while self.runRobotStat == True:
            py, px = self.robot.getPosition()
            state = self.robotGetState()
            #      2
            #     ___
            #  1 |   | 4
            #    |   |
            #0
            #1 forward
            if state == 1:
                self.robotForward()
            #2 turnright
            elif state == 2:
                self.robotTurnRight()
            #3 turnright
            elif state == 3:
                self.robotTurnRight()
            #4 forward
            elif state == 4:
                self.robotForward() 
            #5 forward
            elif state == 5:
                self.robotForward()
            #6 turnleft
            elif state == 6:
                self.robotTurnLeft()
            #7 turnright turnright
            elif state == 7:
                self.robotTurnRight()
                time.sleep(0.1)
                self.robotTurnRight()
                time.sleep(0.1)
                self.robotForward()

            time.sleep(0.1)            
    
    def robotStop(self):
        self.runRobotStat = False
