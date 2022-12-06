class Board():
    def __init__(self, width, height): # ships passed in as xyrh
        self._width = width
        self._height = height
        self._grid = [[0 for _ in range(width)] for _ in range(height)]
        self._shipHP = 0
        self._sGrid = [[0 for _ in range(width)] for _ in range(height)]
        # In a grid, 0 is an emtpy, 1 is a ship, -1 is a hit ship and -2 is a hit empty.

    def attack(self,x,y): # Index starts at 0. 
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
            return -1
        if self._sGrid[y][x] == -2 : # if already hit
            return -2

    def getShipHP(self): # returns total ship HP
        return self._shipHP

    def addShip(self, ship):
        try:
            if ship[2] == "v":
                for y in range(int(ship[1]), int(ship[1])+int(ship[3])):
                    if self._grid[y][int(ship[0])] == 1:
                        return -1
            elif ship[2] == "h":
                for x in range(int(ship[0]), int(ship[0])+int(ship[3])):
                    if self._grid[int(ship[1])][x] == 1:
                        return -1
        except IndexError:
            return -1

        if ship[2] == "v":
            for y in range(int(ship[1]), int(ship[1])+int(ship[3])):
                self._grid[y][int(ship[0])] = 1
        elif ship[2] == "h":
            for x in range(int(ship[0]), int(ship[0])+int(ship[3])):
                self._grid[int(ship[1])][x] = 1
        self._shipHP += int(ship[3])
        return 1

    def getSBoard(self):
        return self._sGrid

    def __repr__(self):
        rep = ""
        for x in self._grid:
            rep += str(x) + "\n"
        return rep

