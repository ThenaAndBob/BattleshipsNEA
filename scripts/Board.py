class Board():
    def __init__(self, width, height): # ships passed in as xyrh
        self._width = width
        self._height = height
        self._grid = [[0 for _ in range(width)] for _ in range(height)]
        self._shipHP = 0
        self._sGrid = [[0 for _ in range(width)] for _ in range(height)]
        # In a grid, 0 is an emtpy, 1 is a ship, -1 is a hit ship and -2 is a hit empty.

    def clear(self):
        print("DEBUG -- Clearing board")
        self._grid = [[0 for _ in range(self._width)] for _ in range(self._height)]
        self._shipHP = 0
        self._sGrid = [[0 for _ in range(self._width)] for _ in range(self._height)]

    def attack(self,x,y): # Index starts at 0. 
        try:
            if x < 0 or x >= self._width or y < 0 or y >= self._height:
                return -2
        except TypeError as e:
            print(e, x, y, "attack in board class")
        try:
            if self._grid[y][x] == 1: # if hit.
                self._grid[y][x] = -1
                self._sGrid[y][x] = -1
                self._shipHP -= 1
                if self._shipHP == 0: # if total shipHp is 0
                    return 2 # Returing -2 = already hit square, -1 = miss, 1 = hit, 2 = game won
                return 1
        except IndexError:
                return -2
        if self._sGrid[y][x] == 0:  # if empty
            self._sGrid[y][x] = -2
            self._grid[y][x] = -2
            return -1
        if self._sGrid[y][x] == -2 : # if already hit
            return -2
        if self._grid[y][x] == -1:
            return -2

    def addShip(self, ship): # string of 4 numbers
        try:
            if ship[2] == "1":
                for y in range(int(ship[1]), int(ship[1])+int(ship[3])):
                    if self._grid[y][int(ship[0])] == 1:
                        return -1
            elif ship[2] == "0":
                for x in range(int(ship[0]), int(ship[0])+int(ship[3])):
                    if self._grid[int(ship[1])][x] == 1:
                        return -1
        except IndexError as e:
            print(ship, e, "Board class, addShip.")
            return -1

        if ship[2] == "1":
            for y in range(int(ship[1]), int(ship[1])+int(ship[3])):
                self._grid[y][int(ship[0])] = 1
        elif ship[2] == "0":
            for x in range(int(ship[0]), int(ship[0])+int(ship[3])):
                self._grid[int(ship[1])][x] = 1
        else:
            print("Rotation of ship doesn't work")
            return -1
        self._shipHP += int(ship[3])
        return 1

    def getSBoard(self):
        return self._sGrid

    def getBoard(self):
        return self._grid

