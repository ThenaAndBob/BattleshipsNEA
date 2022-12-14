from Player import Player
from ai import AI

class Game():
    ships = [2,3,4,5]
    shipCounts = [0,1,1,1,0]
    width = 10
    height = 10
    specialCounts = [0,0,0,False] # barrage, radar, mine
    players = [Player(width, height, specialCounts), Player(width, height, specialCounts)]


    def __init__(self):
        self._players = Game.players

    def radar(self, playerID):
        board = self._player[playerID].getBoard()
        for y, row in enumerate(board):
            for x, value in enumerate(row):
                if value == 1:
                    return [x,y]

    def attack(self,x,y,playerID, attackType): # Playerd ID = 0 or 1, the player being attacked
        if attackType == 0:
            result = self._players[playerID].attack(x,y) # index starts at 0 
            if isinstance(self._players[(playerID +1)%2], AI):
                self._players[(playerID +1)%2].hitFeedback(result, int(x),int(y))
            return result
        else:
            specialCount = self._players[(playerID+1)%2].getSpecials()
            if specialCount[attackType-1] == 0:
                return -2
            self._players[(playerID+1)%2].decrementSpecial(attackType-1)
            for yCoordinate in range(-1,2):
                for xCoordinate in range(-1,2):
                    result = self._players[playerID].attack(x + xCoordinate, y + yCoordinate)
                    if result == 2:
                        return result
            



    def getSpecialCount(self, playerId):
        return self._players[playerId].getSpecials()

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
    def getWidth():
        return Game.width

    @staticmethod
    def getHeight():
        return Game.height

    @staticmethod
    def getSpecials():
        return Game.specialCounts

    @staticmethod
    def getShips():
        return Game.ships

    @staticmethod
    def getNumShips():
        return len(Game.ships)

    @staticmethod
    def changeShips(shipIndex, newNumShips):
        if newNumShips < 0:
            return -2
        dif = newNumShips - Game.shipCounts[shipIndex]
        if dif > 0:
            for _ in range(dif):
                Game.ships.append(shipIndex+1)
                Game.shipCounts[shipIndex] += 1
        elif dif < 0:
            for _ in range(-dif):
                Game.ships.remove(shipIndex+1)
                Game.shipCounts[shipIndex] -= 1

    @staticmethod
    def changeSpecials(specialIndex, newNumSpecials):
        if newNumSpecials < 0:
            return -2
        dif = newNumSpecials - Game.specialCounts[specialIndex]
        if dif > 0:
            for _ in range(dif):
                Game.specialCounts[specialIndex] += 1
        elif dif < 0:
            for _ in range(-dif):
                Game.specialCounts[specialIndex] -= 1

    @staticmethod
    def changeAI(ai):
        print("Ai:", ai)
        ai = int(ai)
        if ai == 0:
            print("Removing AI")
            Game.players = [Player(Game.width, Game.height, Game.specialCounts), Player(Game.width, Game.height, Game.specialCounts)]
        else:
            print("Adding AI")
            Game.players = [Player(Game.width, Game.height, Game.specialCounts), AI(Game.width, Game.height, ai)]

    @staticmethod
    def changeBoardDimensions(newWidth, newHeight):
        print("New board dimensions", newWidth, newHeight)
        Game.width = newWidth
        Game.height = newHeight
        Game.players = [Player(newWidth, newHeight), Player(newWidth, newHeight)]

        