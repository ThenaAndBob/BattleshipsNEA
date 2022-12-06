import random
from pprint import pprint
import seaborn as sns
import matplotlib.pylab as plt
import numpy as np
import time

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
board = aiSims(board, [5,4,3,2])
t2 = time.perf_counter()

print(t2-t1)

pprint(board)
ax = sns.heatmap(board, linewidth=0.5)
plt.show()
                    
