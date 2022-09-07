class Board():
    def __init__(self, width, height): # ships passed in as xyrh
        self._width = width
        self._height = height
        self._grid = [[0 for _ in range(width)] for _ in range(height)]
        self._ships = []
        self._shipHP = 0
        # In grid, a 0 is empty, 1 is ship, -1 is hit ship.

    def attack(self,x,y): # Index starts at 0.
        if self._grid[y][x] == 1:
            self._grid[y][x] = -1
            self._shipHP -= 1
            if self._shipHP == 0:
                return 2
            return 1
        return self._grid[y][x]

    def shipHP(self): # returns total ship HP
        return self._shipHP

    def addShip(self, ship):
        self._ships.append(ship)
        if ship[2] == "v":
            for y in range(int(ship[1]), int(ship[1])+int(ship[3])):
                self._grid[y][int(ship[0])] = 1
        elif ship[2] == "h":
            for x in range(int(ship[0]), int(ship[0])+int(ship[3])):
                self._grid[int(ship[1])][x] = 1
        self._shipHP += int(ship[3])

    def __repr__(self):
        rep = ""
        for x in self._grid:
            rep += str(x) + "\n"
        return rep

