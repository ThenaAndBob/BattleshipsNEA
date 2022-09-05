from Player import Player

class Game():
    def __init__(self):
        self._players = [Player() for _ in range(2)]

    def Attack(self,x,y,playerID):
        self._players[playerID].attack(x,y)

    def getNumShips(self,playerID):
        self._players[playerID].getNumShips()
        


        