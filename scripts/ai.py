from pprint import pprint 
import random
import seaborn as sns
import matplotlib.pylab as plt
import numpy as np

# game area
width = 10
height = 10
gA = [[0] * width for _ in range(height)]

# sim stats
sims = 10000
numShips = 10
size = 3
# dirs = [up, right, down, left]

for _ in range(sims):
    taken = []
    for _ in range(numShips):
        while True:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            dir = random.randint(0, 3)
            if dir == 0:
                if y - size >= -1:
                    for c in range(size):
                        if (y - c,x) in taken:
                            break
                    else:
                        for c in range(size):
                            gA[y - c][x] += 1
                            taken.append((y - c,x))
                        break
            elif dir == 1:
                if x + size <= width:
                    for c in range(size):
                        if (y,x+c) in taken:
                            break
                    else:
                        for c in range(size):
                            gA[y][x+c] += 1
                            taken.append((y,x+c))
                        break
            elif dir == 2:
                if y + size <= height:
                    for c in range(size):
                        if (y+c,x) in taken:
                            break
                    else:
                        for c in range(size):
                            gA[y+c][x] += 1
                            taken.append((y+c,x))
                        break
            elif dir == 3:
                if x - size >= -1:
                    for c in range(size):
                        if (y,x-c) in taken:
                            break
                    else:
                        for c in range(size):
                            gA[y][x-c] += 1
                            taken.append((y,x-c))
                        break

max = np.amax(gA)
print(max)
for y in range(height):
    go = False
    for x in range(width):
        if gA[y][x] == max:
            print(x,y)
            break
    else:
        go = True
    if not go:
        break

pprint(gA)
ax = sns.heatmap(gA, linewidth=0.5)
plt.show()
