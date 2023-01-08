from Board import Board

class Player():
    def __init__(self, width, height, specialCounts):
        self._board = Board(width, height)
        self._ships = [] # ships stored as [[hp, [xCoord, yCoord], [xCoord, yCoord]...] ... ]
        self._specialCounts = specialCounts.copy() # a list of the number of specials the player has left, format: [barrageCount, radarCount, mineCount, hitStreak]
        print("Creating player object")
        print(f"Speicals - {self._specialCounts}")

    def clearBoard(self):
        self._board.clear()

    def getHP(self):
        return self._board.getHP()

    def attack(self, x,y): # index starts at 0
        result = self._board.attack(x,y)
        if result == 1:
            for ship in self._ships:
                if [x,y] in ship:
                    ship.remove([x,y])
                    if len(ship) == 1:
                        self._ships.remove(ship)
        return result

    def addShip(self, ship):
        result = self._board.addShip(ship)
        if result != -1:
            self._ships.append([int(ship[3])])
            if ship[2] == "1":
                for y in range(int(ship[1]), int(ship[1])+int(ship[3])):
                    self._ships[-1].append( [int(ship[0]), y] )
            elif ship[2] == "0":
                for x in range(int(ship[0]), int(ship[0])+int(ship[3])):
                    self._ships[-1].append( [x, int(ship[1])] )
        else:
            return result

    def getBoard(self):
        return self._board.getBoard()

    def getSBoard(self):
        return self._board.getSBoard()

    def getShips(self):
        re = []
        for ship in self._ships:
            re.append(ship[0])
        return re

    def getSpecials(self):
        return self._specialCounts

    def decrementSpecial(self, specialIndex):
        print(f"DEBUG -- Decrementing special attack")
        self._specialCounts[specialIndex] -= 1