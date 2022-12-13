from Player import Player
import random

class AI(Player):
    def __init__(self, width, height, difficulty):
        super().__init__(width, height)
        self._difficulty = difficulty
        self._hit = False

    def __validDirections(self, shipLength, xCoordinate, yCoordinate):
        valid_directions = 0
        for direction in [[1,0],[-1,0],[0,1],[0,-1]]:
            checkX = xCoordinate
            checkY = yCoordinate
            for _ in range(shipLength):
                if checkX < 0 or checkX >= len(self._board[0]) or checkY < 0 or checkY >= len(self._board):
                    valid_directions -= 1
                    break
                elif self._board[checkY][checkX] != 0:
                    valid_directions -= 1
                    break
                checkX += direction[0]
                checkY += direction[1]
                
            valid_directions += 1
        return valid_directions

    def getAttack(self, ships):
        probabiltyBoard = [[0 for _ in range(len(self._board))] for _ in range(len(self._board[0]))]
        for ship in ships:
            for yC in range(len(self._board)):
                for xC in range(len(self._board[yC])):
                    probabiltyBoard[yC][xC] += self.__validDirections(ship, xC, yC)
        return probabiltyBoard

    def getShipPlacement(self, shipLength):
        return f"{random.randrange(0, self._bWidth)}{random.randrange(0, self._bHeight)}{random.randrange(0, 2)}{shipLength}"




                    
