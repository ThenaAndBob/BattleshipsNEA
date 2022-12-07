from Player import Player

class Game():
    def __init__(self):
        self._players = [Player(), Player()]

    def attack(self,x,y,playerID): # Playerd ID = 0 or 1
        return self._players[playerID].attack(x,y) # index starts at 0 

    def getPlayer(self, playerID):
        return self._players[playerID]
        
    def addShip(self, pNum, ship):
        return self._players[pNum].addShip(ship)

    def getBoard(self, pNum):
        return self._players[pNum].getBoard()

    def getSBoard(self,pNum):
        return self._players[pNum].getSBoard()


        