from Player import Player

class Game():
    def __init__(self):
        self._players = [Player(0), Player(1)]

    def Attack(self,x,y,playerID): # Playerd ID = 0 or 1
        return self._players[playerID].attack(x,y) # index starts at 0

    def getNumShips(self,playerID):
        self._players[playerID].getNumShips()   

    def getPlayer(self, playerID):
        return self._players[playerID]
        
    def addShip(self, pNum, ship):
        self._players[pNum].addShip(ship)

    def getBoard(self, pNum):
        return self._players[pNum].getBoard()


        