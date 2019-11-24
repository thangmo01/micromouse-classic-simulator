import tkinter as tk
import time
import queue

from robot import Robot
from wall import VerticalWall, HorizontalWall
from block import Block

class Field(tk.Frame):
    def __init__(self, parent, rowNum = 16, colNum = 16):
        tk.Frame.__init__(self, parent)
        self.runRobotStat = False
        self.rowNum = rowNum
        self.colNum = colNum

        self.targets = []
        
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
        from map import initflood

        for r in range(self.rowNum):
            for c in range(self.colNum):
                self.vwalls[r][c] = VerticalWall(self)
                self.vwalls[r][c].grid(row=r*2 + 1, column=c*2)
                self.hwalls[r][c] = HorizontalWall(self)
                self.hwalls[r][c].grid(row=r*2, column=c*2 + 1)
                self.blocks[r][c] = Block(self, row=r*2 + 1, col=c*2 + 1)
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

    def setTarget(self, targets = []):
        self.targets = targets
        for target in targets:
            self.blocks[target[0]][target[1]].setTargetBlock()

    def setStart(self, start = (0,0)):
        self.setRobot(start[0], start[1])
        self.start = start

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

    def robotGetState(self, vwalls, hwalls):
        py, px = self.robot.getPosition()
        state = 0
        d = self.robot.getDirection()
        if d == 'N':
            if self.vwalls[py][px].have == True:
                vwalls[py][px] = True
                self.vwalls[py][px].setRedWall()
                state += 1
            if self.hwalls[py][px].have == True:
                hwalls[py][px] = True
                self.hwalls[py][px].setRedWall()
                state += 2
            if self.vwalls[py][px + 1].have == True:
                vwalls[py][px + 1] == True
                self.vwalls[py][px + 1].setRedWall()
                state += 4
        elif d == 'E':
            if self.hwalls[py][px].have == True:
                self.hwalls[py][px].setRedWall()
                hwalls[py][px] = True
                state += 1
            if self.vwalls[py][px + 1].have == True:
                self.vwalls[py][px + 1].setRedWall()
                vwalls[py][px + 1] = True
                state += 2
            if self.hwalls[py + 1][px].have == True:
                self.hwalls[py + 1][px].setRedWall()
                hwalls[py + 1][px] = True
                state += 4
        elif d == 'S':
            if self.vwalls[py][px + 1].have == True:
                self.vwalls[py][px + 1].setRedWall()
                vwalls[py][px + 1] = True
                state += 1
            if self.hwalls[py + 1][px].have == True:
                self.hwalls[py + 1][px].setRedWall()
                hwalls[py + 1][px] = True
                state += 2
            if self.vwalls[py][px].have == True:
                self.vwalls[py][px].setRedWall()
                vwalls[py][px] = True
                state += 4
        elif d == 'W':
            if self.hwalls[py + 1][px].have == True:
                self.hwalls[py + 1][px].setRedWall()
                hwalls[py + 1][px] = True
                state += 1
            if self.vwalls[py][px].have == True:
                self.vwalls[py][px].setRedWall()
                vwalls[py][px] = True
                state += 2
            if self.hwalls[py][px].have == True:
                self.hwalls[py][px].setRedWall()
                hwalls[py][px] = True
                state += 4

        return state

    def robotFoundTarget(self, complete):
        py, px = self.robot.getPosition()
        i = 0
        for target in self.targets:
            if py == target[0] and px == target[1]:
                complete[i] = True
                return True
            i += 1
        return False
    
    def robotFoundStart(self):
        py, px = self.robot.getPosition()
        if py == self.start[0] and px == self.start[1]:
            return True
        else:
            return False

    def robotMapping(self):
        #create empty vwalls
        vwalls = [False] * self.rowNum
        for i in range(self.rowNum):
            vwalls[i] = [False] * (self.colNum+1)

        #create empty hwalls
        hwalls = [False] * (self.rowNum+1)
        for i in range(self.rowNum+1):
            hwalls[i] = [False] * self.colNum
            
        flag = [False] * self.rowNum
        marking = [False] * self.rowNum
        count = [0] * self.rowNum
        for i in range(self.rowNum):
            flag[i] = [False] * self.colNum
            marking[i] = [False] * self.colNum
            count[i] = [0] * self.colNum

        self.runRobotStat = True
        foundCentre = [False] * 4#to check found 4 block of centre  
        
        while self.runRobotStat == True and foundCentre.count(True) != 4:
            self.robotDecisionFindTarget(vwalls, hwalls)
            self.resetBlockValue()
            self.flood(vwalls, hwalls)

            self.robotFoundTarget(foundCentre)

        while self.runRobotStat == True and self.robotFoundStart() == False:
            self.robotDecisionFindHome(vwalls, hwalls)
            self.resetBlockValue()
            self.flood(vwalls, hwalls)
        
        '''
        for i in range(self.rowNum + 1):
            for j in range(self.colNum):
                hwalls[i][j] = self.hwalls[i][j].getWall()

        for i in range(self.rowNum):
            for j in range(self.colNum + 1):
                vwalls[i][j] = self.vwalls[i][j].getWall()
        '''
    
    def robotDecisionFindHome(self, vwalls, hwalls):
        py, px = self.robot.getPosition()
        if self.blocks[py][px].flag == True:
            self.blocks[py][px].count += 1
        self.blocks[py][px].flag = True

        over = False
        if self.blocks[py][px].count > 4:
            over = True

        state = self.robotGetState(vwalls, hwalls)
        #      2
        #     ___
        #  1 |   | 4
        #    |   |
        #0 3-Way
        if state == 0:
            left, front, right = self.getBlock(py, px, sf=(True, True, True))
            if front['flag'] == False and front['mark'] == False:
                self.robotForward()
            elif right['flag'] == False and right['mark'] == False:
                self.robotTurnRight()
            elif left['flag'] == False and left['mark'] == False:
                self.robotTurnLeft()
            elif over and front['count'] <= right['count'] and front['count'] <= left['count']:
                self.robotForward()
            elif over and right['count'] <= front['count'] and right['count'] <= left['count']:
                self.robotTurnRight()
            elif over and left['count'] <= front['count'] and left['count'] <= right['count']:
                self.robotTurnLeft()
            elif front['value'] >= right['value'] and front['value'] >= left['value']:
                self.robotForward()
            elif right['value'] >= front['value'] and right['value'] >= left['value']:
                self.robotTurnRight()
            else:
                self.robotTurnLeft()
        #1 2-Way
        elif state == 1:
            #compare potential between front and right
            front, right = self.getBlock(py, px, sf=(False, True, True))
            
            if front['flag'] == False and front['mark'] == False:
                self.robotForward()
            elif right['flag'] == False and right['mark'] == False:
                self.robotTurnRight()
            elif over and front['count'] <= right['count']:
                self.robotForward()
            elif over and right['count'] <= front['count']:
                self.robotTurnRight()
            elif front['value'] >= right['value']:
                self.robotForward()
            else:
                self.robotTurnRight()
        #2 2-Way
        elif state == 2:
            #compare potential between left and right
            left, right = self.getBlock(py, px, sf=(True, False, True))
            if right['flag'] == False and right['mark'] == False:
                self.robotTurnRight()
            elif left['flag'] == False and left['mark'] == False:
                self.robotTurnLeft()
            elif over and right['count'] <= left['count']:
                self.robotTurnRight()
            elif over and left['count'] <= right['count']:
                self.robotTurnLeft()
            elif right['value'] >= left['value']:
                self.robotTurnRight()
            else:
                self.robotTurnLeft()
        #4 2-Way
        elif state == 4:
            #compare potential between front and left
            left, front = self.getBlock(py, px, sf=(True, True, False))
            if front['flag'] == False and front['mark'] == False:
                self.robotForward()
            elif left['flag'] == False and left['mark'] == False:
                self.robotTurnLeft()
            elif over and front['count'] <= left['count']:
                self.robotForward()
            elif over and left['count'] <= front['count']:
                self.robotTurnLeft()
            elif front['value'] >= left['value']:
                self.robotForward()
            else:
                self.robotTurnLeft()
        #3 1-Way
        elif state == 3:
            self.robotTurnRight()
        #5 1-Way
        elif state == 5:
            self.robotForward()
        #6 1-Way
        elif state == 6:
            self.robotTurnLeft()
        #7 0-Way
        elif state == 7:
            self.blocks[py][px].mark = True

            self.robotTurnRight()
            time.sleep(0.05)
            self.robotTurnRight()

        time.sleep(0.05)

    def robotDecisionFindTarget(self, vwalls, hwalls):
        py, px = self.robot.getPosition()
        if self.blocks[py][px].flag == True:
            self.blocks[py][px].count += 1
        self.blocks[py][px].flag = True

        over = False
        if self.blocks[py][px].count > 4:
            over = True

        state = self.robotGetState(vwalls, hwalls)
        #      2
        #     ___
        #  1 |   | 4
        #    |   |
        #0 3-Way
        if state == 0:
            left, front, right = self.getBlock(py, px, sf=(True, True, True))
            if front['flag'] == False and front['mark'] == False:
                self.robotForward()
            elif right['flag'] == False and right['mark'] == False:
                self.robotTurnRight()
            elif left['flag'] == False and left['mark'] == False:
                self.robotTurnLeft()
            elif over and front['count'] <= right['count'] and front['count'] <= left['count']:
                self.robotForward()
            elif over and right['count'] <= front['count'] and right['count'] <= left['count']:
                self.robotTurnRight()
            elif over and left['count'] <= front['count'] and left['count'] <= right['count']:
                self.robotTurnLeft()
            elif front['value'] <= right['value'] and front['value'] <= left['value']:
                self.robotForward()
            elif right['value'] <= front['value'] and right['value'] <= left['value']:
                self.robotTurnRight()
            else:
                self.robotTurnLeft()
        #1 2-Way
        elif state == 1:
            #compare potential between front and right
            front, right = self.getBlock(py, px, sf=(False, True, True))
            
            if front['flag'] == False and front['mark'] == False:
                self.robotForward()
            elif right['flag'] == False and right['mark'] == False:
                self.robotTurnRight()
            elif over and front['count'] <= right['count']:
                self.robotForward()
            elif over and right['count'] <= front['count']:
                self.robotTurnRight()
            elif front['value'] <= right['value']:
                self.robotForward()
            else:
                self.robotTurnRight()
        #2 2-Way
        elif state == 2:
            #compare potential between left and right
            left, right = self.getBlock(py, px, sf=(True, False, True))
            if right['flag'] == False and right['mark'] == False:
                self.robotTurnRight()
            elif left['flag'] == False and left['mark'] == False:
                self.robotTurnLeft()
            elif over and right['count'] <= left['count']:
                self.robotTurnRight()
            elif over and left['count'] <= right['count']:
                self.robotTurnLeft()
            elif right['value'] <= left['value']:
                self.robotTurnRight()
            else:
                self.robotTurnLeft()
        #4 2-Way
        elif state == 4:
            #compare potential between front and left
            left, front = self.getBlock(py, px, sf=(True, True, False))
            if front['flag'] == False and front['mark'] == False:
                self.robotForward()
            elif left['flag'] == False and left['mark'] == False:
                self.robotTurnLeft()
            elif over and front['count'] <= left['count']:
                self.robotForward()
            elif over and left['count'] <= front['count']:
                self.robotTurnLeft()
            elif front['value'] <= left['value']:
                self.robotForward()
            else:
                self.robotTurnLeft()
        #3 1-Way
        elif state == 3:
            self.robotTurnRight()
        #5 1-Way
        elif state == 5:
            self.robotForward()
        #6 1-Way
        elif state == 6:
            self.robotTurnLeft()
        #7 0-Way
        elif state == 7:
            self.blocks[py][px].mark = True

            self.robotTurnRight()
            time.sleep(0.05)
            self.robotTurnRight()

        time.sleep(0.05)            

    def getBlock(self, py, px, sf=(True, True, True)):
        d = self.robot.getDirection()
        #sf = (left, front, right)
        #return (left, front, right)
        if d == 'N':
            if sf[0] and sf[1] and sf[2]:
                return (self.blocks[py][px - 1].getBlockInfo(), self.blocks[py - 1][px].getBlockInfo(), self.blocks[py][px + 1].getBlockInfo())
            if sf[1] and sf[2]:
                return (self.blocks[py - 1][px].getBlockInfo(), self.blocks[py][px + 1].getBlockInfo())
            if sf[0] and sf[1]:
                return (self.blocks[py][px - 1].getBlockInfo(), self.blocks[py - 1][px].getBlockInfo())
            if sf[0] and sf[2]:
                return (self.blocks[py][px - 1].getBlockInfo(), self.blocks[py][px + 1].getBlockInfo())

        if d == 'E':
            if sf[0] and sf[1] and sf[2]:
                return (self.blocks[py - 1][px].getBlockInfo(), self.blocks[py][px + 1].getBlockInfo(), self.blocks[py + 1][px].getBlockInfo())
            if sf[1] and sf[2]:
                return (self.blocks[py][px + 1].getBlockInfo(), self.blocks[py + 1][px].getBlockInfo())
            if sf[0] and sf[1]:
                return (self.blocks[py - 1][px].getBlockInfo(), self.blocks[py][px + 1].getBlockInfo())
            if sf[0] and sf[2]:
                return (self.blocks[py - 1][px].getBlockInfo(), self.blocks[py + 1][px].getBlockInfo())

        if d == 'S':
            if sf[0] and sf[1] and sf[2]:
                return (self.blocks[py][px + 1].getBlockInfo(), self.blocks[py + 1][px].getBlockInfo(), self.blocks[py][px - 1].getBlockInfo())
            if sf[1] and sf[2]:
                return (self.blocks[py + 1][px].getBlockInfo(), self.blocks[py][px - 1].getBlockInfo())
            if sf[0] and sf[1]:
                return (self.blocks[py][px + 1].getBlockInfo(), self.blocks[py + 1][px].getBlockInfo())
            if sf[0] and sf[2]:
                return (self.blocks[py][px + 1].getBlockInfo(), self.blocks[py][px - 1].getBlockInfo())

        if d == 'W':
            if sf[0] and sf[1] and sf[2]:
                return (self.blocks[py + 1][px].getBlockInfo(), self.blocks[py][px - 1].getBlockInfo(), self.blocks[py - 1][px].getBlockInfo())
            if sf[1] and sf[2]:
                return (self.blocks[py][px - 1].getBlockInfo(), self.blocks[py - 1][px].getBlockInfo())
            if sf[0] and sf[1]:
                return (self.blocks[py + 1][px].getBlockInfo(), self.blocks[py][px - 1].getBlockInfo())
            if sf[0] and sf[2]:
                return (self.blocks[py + 1][px].getBlockInfo(), self.blocks[py - 1][px].getBlockInfo())

    def flood(self, vwalls, hwalls):
        q = queue.Queue(self.colNum * self.rowNum)

        for target in self.targets:
            y, x = target
            q.put((y, x, 0))
            self.blocks[y][x].setValue(0)
        
        while not q.empty():
            y, x, v = q.get()
            #North
            if y - 1 >= 0 and hwalls[y][x] == False and self.blocks[y - 1][x].getValue() == -1:
                self.blocks[y - 1][x].setValue(v + 1)
                q.put((y - 1, x, v + 1))
            #East
            if x + 1 < 16 and vwalls[y][x + 1] == False and self.blocks[y][x + 1].getValue() == -1:
                self.blocks[y][x + 1].setValue(v + 1)
                q.put((y, x + 1, v + 1))
            #South
            if y + 1 < 16 and hwalls[y + 1][x] == False and self.blocks[y + 1][x].getValue() == -1:
                self.blocks[y + 1][x].setValue(v + 1)
                q.put((y + 1, x, v + 1))
            #West
            if x - 1 >= 0 and vwalls[y][x] == False and self.blocks[y][x - 1].getValue() == -1:
                self.blocks[y][x - 1].setValue(v + 1)
                q.put((y, x - 1, v + 1))

    def resetBlockValue(self):
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[i])):
                self.blocks[i][j].setValue(-1)

    def robotShortesPath(self):
        pass

    def robotRun(self):
        self.robotMapping()

    def robotStop(self):
        self.runRobotStat = False
