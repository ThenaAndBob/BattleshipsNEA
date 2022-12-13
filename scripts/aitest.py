import numpy as np
from pprint import pprint
import time

class AI(): # DO NOT USE THIS, USE AITEST I BEG OF YOU
    def __init__(self):
        self.SHIP_SIZES = [2,3,4,5]
        self.SHOT_MAP = np.zeros([10, 10])

    def gen_prob_map(self):
        prob_map = np.zeros([10, 10])
        for ship_size in self.SHIP_SIZES:
            use_size = ship_size - 1
            for row in range(10):
                for col in range(10):
                    if self.SHOT_MAP[row][col] != 1:
                        endpoints = []
                        if row - use_size >= 0:
                            endpoints.append(((row - use_size, col), (row + 1, col + 1)))
                        if row + use_size <= 9:
                            endpoints.append(((row, col), (row + use_size + 1, col + 1)))
                        if col - use_size >= 0:
                            endpoints.append(((row, col - use_size), (row + 1, col + 1)))
                        if col + use_size <= 9:
                            endpoints.append(((row, col), (row + 1, col + use_size + 1)))
                        pprint(endpoints)
                        for (start_row, start_col), (end_row, end_col) in endpoints:
                            if np.all(self.SHOT_MAP[start_row:end_row, start_col:end_col] == 0):
                                prob_map[start_row:end_row, start_col:end_col] += 1
        return prob_map

timeS = time.perf_counter()
myAI = AI()
pprint(myAI.gen_prob_map())
print(time.perf_counter() - timeS)

import random
from pprint import pprint
import seaborn as sns
import matplotlib.pylab as plt
import numpy as np
import time

class AI():
    pass

def validDirections(board, shipLength, xCoordinate, yCoordinate):
    valid_directions = 0
    for direction in [[1,0],[-1,0],[0,1],[0,-1]]:
        checkX = xCoordinate
        checkY = yCoordinate
        for _ in range(shipLength):
            if checkX < 0 or checkX >= len(board[0]) or checkY < 0 or checkY >= len(board):
                valid_directions -= 1
                break
            elif board[checkY][checkX] != 0:
                valid_directions -= 1
                break
            checkX += direction[0]
            checkY += direction[1]
            
        valid_directions += 1
    return valid_directions


def rotationalSim(board, ships):
    probabiltyBoard = [[0 for _ in range(len(board))] for _ in range(len(board[0]))]
    for ship in ships:
        for yC in range(len(board)):
            for xC in range(len(board[yC])):
                probabiltyBoard[yC][xC] += validDirections(board, ship, xC, yC)
    return probabiltyBoard


def isValid(direction, yC, xC, taken, shipLength, width, height):
    if direction == 0 or direction == 2:
        if direction == 0:
            yC -= shipLength - 1
        if yC < 0 or yC + shipLength - 1 >= height:
            return False
        for i in range(shipLength):
            if [yC+i,xC] in taken:
                return False
    elif direction == 1 or direction == 3:
        if direction == 3:
            xC -= shipLength - 1
        if xC < 0 or xC + shipLength - 1 >= width:
            return False
        for i in range(shipLength):
            if [yC,xC+i] in taken:
                return False
    return True

def aiSims(board, ships): # ships is a list of ints, since we only need the length of each ship.
    sims = 100000
    finalBoard = [[0 for _ in range(10)] for _ in range (10)]
    taken = []
    for yi, y, in enumerate(board):
        for xi, x in enumerate(y):
            if x != 0:
                taken.append([yi,xi])
    
    height = len(board)
    width = len(board[0])
    for _ in range(sims):
        tempTaken = taken.copy()
        for shipLength in ships:
            direction = random.randint(0,3)
            xC, yC = random.randrange(0,width), random.randrange(0,height)

            if isValid(direction, yC, xC, tempTaken, shipLength, width, height):
                if direction == 0 or direction == 2:
                    if direction == 0:
                        yC -= shipLength - 1
                        for i in range(shipLength):
                            finalBoard[yC+i][xC] += 1
                            tempTaken.append([yC+i, xC])
                            
                if direction == 1 or direction == 3:
                    if direction == 3:
                        xC -= shipLength - 1
                    for i in range(shipLength):
                        finalBoard[yC][xC+i] += 1
                        tempTaken.append([yC, xC+i])
    return finalBoard

t1 = time.perf_counter()
board = [[0 for _ in range(10)] for _ in range (10)]
board[5][5] = 1
board = rotationalSim(board, [5,4,3,2])
t2 = time.perf_counter()

print(t2-t1)

pprint(board)
ax = sns.heatmap(board, linewidth=0.5)
plt.show()
                    
