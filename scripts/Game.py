from Player import Player
from ai import AI

class Game():
    ships = [5,4,3,2]
    width = 10
    height = 10
    players = [Player(width, height), Player(width, height)]


    def __init__(self):
        self._players = Game.players

    def attack(self,x,y,playerID): # Playerd ID = 0 or 1
        result = self._players[playerID].attack(x,y) # index starts at 0 
        if isinstance(self._players[(playerID +1)%2], AI):
                self._players[(playerID +1)%2].hitFeedback(result, int(x),int(y))
        return result

    def getPlayer(self, playerID):
        return self._players[playerID]
        
    def addShip(self, pNum, ship):
        return self._players[pNum].addShip(ship)

    def getBoard(self, pNum):
        return self._players[pNum].getBoard()

    def getSBoard(self,pNum):
        return self._players[pNum].getSBoard()

    def getAIShip(self, shipIndex):
        return self._players[1].getShipPlacement(Game.ships[shipIndex])

    def getAIAttack(self):
        print(self._players[0].getShips())
        return self._players[1].getAttack(self._players[0].getShips(), self._players[0].getSBoard())

    @staticmethod
    def getNumShips():
        return len(Game.ships)

    @staticmethod
    def addStartShip(ship):
        print("Ship added:", ship)
        Game.ships.append(ship)
    
    @staticmethod
    def delShip(ship):
        Game.ships.remove(ship)

    @staticmethod
    def changeAI(ai):
        print("Ai:", ai)
        ai = int(ai)
        if ai == 0:
            print("Removing AI")
            Game.players = [Player(Game.width, Game.height), Player(Game.width, Game.height)]
        else:
            print("Adding AI")
            Game.players = [Player(Game.width, Game.height), AI(Game.width, Game.height, ai)]

    @staticmethod
    def changeBoardDimensions(newWidth, newHeight):
        print("New board dimensions", newWidth, newHeight)
        Game.width = newWidth
        Game.height = newHeight
        Game.players = [Player(newWidth, newHeight), Player(newWidth, newHeight)]

        