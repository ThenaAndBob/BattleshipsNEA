from Player import Player
from ai import AI

class Game():
    ships = [2,3,4,5]
    shipCounts = [0,1,1,1,1,0]
    width = 10
    height = 10
    specialCounts = [0,0,0,0,0] # barrage, radar, mine, hitstreak, hints
    numPlayers = 2
    players = [Player(width, height, specialCounts), Player(width, height, specialCounts)]

    def __init__(self):
        #########################################################################
        #
        # CATEGORY A SKILL: Composition
        # A game has player objects stored in a list.
        #
        #########################################################################
        self._players = Game.players

    def clearBoard(self, playerNum):
        self._players[playerNum].clearBoard()

    def radar(self, playerNum, attacker=None):
        if attacker is None:
            attacker = (playerNum+1)%2
        specialCount = self._players[attacker].getSpecials()
        if specialCount[1] == 0:
            return []
        board = self._players[playerNum].getBoard()
        self._players[attacker].decrementSpecial(1)
        for y, row in enumerate(board):
            for x, value in enumerate(row):
                if value == 1:
                    return [x,y]

    def attack(self,x,y,playerNum, attackType, attacker=None): # PlayerNum ID = 0 or 1, the player being attacked
        if attacker is None:
            attacker = (playerNum+1)%2
        print(f"Attacking player {playerNum} with attackType {attackType} at {x}, {y}")
        if attackType == 0:
            result = self._players[playerNum].attack(x,y) # index starts at 0 
            if isinstance(self._players[attacker], AI):
                self._players[attacker].hitFeedback(result, int(x),int(y))
            return result
        elif attackType == 1:
            specialCount = self._players[attacker].getSpecials()
            if specialCount[attackType-1] == 0:
                return -2
            self._players[attacker].decrementSpecial(attackType-1)
            for yCoordinate in range(-1,2):
                for xCoordinate in range(-1,2):
                    result = self._players[playerNum].attack(x + xCoordinate, y + yCoordinate)
                    if result == 2:
                        return result
            
    def getSpecialCount(self, playerNum):
        return self._players[playerNum].getSpecials()
     
    def addShip(self, pNum, ship):
        try:
            ship = list(map(int, ship))
        except ValueError:
            return -1
        return self._players[pNum].addShip(ship)

    def getBoard(self, pNum):
        return self._players[pNum].getBoard()

    def getSBoard(self,pNum):
        return self._players[pNum].getSBoard()

    def getAIShip(self, shipIndex):
        print("index in ai", shipIndex)
        try:
            return self._players[1].getShipPlacement(Game.ships[shipIndex])
        except Exception as e:
            print(self._players)
            print(shipIndex)
            print(Game.ships)
            input(e)

    def getHP(self, pNum):
        return self._players[pNum].getHP()

    def getAIAttack(self):
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
    def updatePlayers():
        Game.players = [Player(Game.width, Game.height, Game.specialCounts) for _ in range(Game.numPlayers)]

    @staticmethod
    def getNumShips():
        return len(Game.ships)

    @staticmethod
    def changeShips(shipIndex, newNumShips):
        if newNumShips < 0:
            return -2
        try:
            dif = newNumShips - Game.shipCounts[shipIndex]
        except IndexError as e:
            print(shipIndex, Game.shipCounts)
            raise e
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
        ai = int(ai)
        if ai == 0:
            Game.players = [Player(Game.width, Game.height, Game.specialCounts) for _ in range(Game.numPlayers)]
        else:
            Game.players = [Player(Game.width, Game.height, Game.specialCounts), AI(Game.width, Game.height, ai)]   
            Game.numPlayers = 2

    @staticmethod
    def changeBoardDimensions(newWidth, newHeight):
        Game.width = newWidth
        Game.height = newHeight
        Game.players = [Player(newWidth, newHeight, Game.specialCounts), Player(newWidth, newHeight, Game.specialCounts)]

    @staticmethod
    def changeNumPlayers(newNumPlayers):
        Game.numPlayers = newNumPlayers
        if newNumPlayers != 2:
            Game.changeAI(0) # Updates Game.players

    @staticmethod
    def getNumPlayers():
        return Game.numPlayers        