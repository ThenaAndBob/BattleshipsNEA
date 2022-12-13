from Player import Player
import random
import numpy as np

class AI(Player):
    def __init__(self, width, height, difficulty):
        super().__init__(width, height)
        self._difficulty = difficulty
        self._hit = None
        self._directions = [[0,-1], [1,0], [0,1], [-1,0]]
        self._sides = 0

    def __validDirections(self, board, shipLength, xCoordinate, yCoordinate):
        valid_directions = 0
        for direction in [[1,0],[-1,0],[0,1],[0,-1]]:
            checkX = xCoordinate
            checkY = yCoordinate
            for _ in range(shipLength):
                if checkX < 0 or checkX >= len(board[0]) or checkY < 0 or checkY >= len(board):
                    valid_directions -= 1
                    break
                elif board[checkY][checkX] != 0:
                    valid_directions -= 1
                    break
                checkX += direction[0]
                checkY += direction[1]
                
            valid_directions += 1
        return valid_directions

    def getAttack(self, ships, board):
        if self._hit is None:
            print("normal attacking")
            probabiltyBoard = [[0 for _ in range(len(board))] for _ in range(len(board[0]))]
            for ship in ships:
                for yC in range(len(board)):
                    for xC in range(len(board[yC])):
                        probabiltyBoard[yC][xC] += self.__validDirections(board, ship, xC, yC)

            maxValue = np.amax(probabiltyBoard)
            for y, row in enumerate(probabiltyBoard):
                for x, value in enumerate(row):
                    if value == maxValue:
                        print("AI attacked:",x,y)
                        return [x,y]
            print("Something went wrong with AI attack subroutine")
        else:
            print("ortogonal strat")
            x = self._hit[0] + (self._hit[3] * self._directions[self._hit[2]][0])
            y = self._hit[1] + (self._hit[3] * self._directions[self._hit[2]][1])
            while board[y][x] == -1:
                self._hit[3] += 1
                x = self._hit[0] + (self._hit[3] * self._directions[self._hit[2]][0])
                y = self._hit[1] + (self._hit[3] * self._directions[self._hit[2]][1])

            print("AI attacked:",x,y)
            print(self._hit)
            return [x,y]

    def getShipPlacement(self, shipLength):
        return f"{random.randrange(0, self._bWidth)}{random.randrange(0, self._bHeight)}{random.randrange(0, 2)}{shipLength}"

    def hitFeedback(self,result, x,y):
        if self._hit is None and result == 1:
            self._hit = [x,y,0,1]
        elif self._hit is not None:
            if result == 1: # The orthogonal attack was a hit
                self._hit[3] += 1
            elif self._sides == 1: # it was a miss and we should turn around
                self._sides = 0 # The ship has been cleared out.
                self._hit = None
            else: # it was a miss
                if self._hit[3] > 1:
                    self._hit[2] = (self._hit[2] + 2) % 4
                    self._hit[3] = 1
                    self._sides += 1
                else:
                    print("hit incremented")
                    self._hit[2] += 1






                    
