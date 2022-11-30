from Board import Board

class Player():
    def __init__(self): # 0 or 1
        self._board = Board(10,10)

    def attack(self, x,y): # index starts at 0
        return self._board.attack(x,y)

    def addShip(self, ship):
        return self._board.addShip(ship)

    def getBoard(self):
        return self._board

    def getName(self):
        return self._name

    def getSBoard(self):
        return self._board.getSBoard()
