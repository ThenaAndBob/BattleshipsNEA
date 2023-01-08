from Player import Player
import random
import numpy as np

class AI(Player):
    def __init__(self, width, height, difficulty):
        super().__init__(width, height, [0,0,0,0])
        self._difficulty = difficulty
        self._hit = None
        self._directions = [(0,-1), (1,0), (0,1), (-1,0)]
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

    def __isValid(self, direction, yC, xC, taken, shipLength, width, height):
        if direction == 0 or direction == 2:
            if direction == 0:
                yC -= shipLength - 1
            if yC < 0 or yC + shipLength - 1 >= height:
                return False
            for i in range(shipLength):
                if [yC+i,xC] in taken:
                    return False
        elif direction == 1 or direction == 3:
            if direction == 3:
                xC -= shipLength - 1
            if xC < 0 or xC + shipLength - 1 >= width:
                return False
            for i in range(shipLength):
                if [yC,xC+i] in taken:
                    return False
        return True

    def __chooseAttackSquare(self, probabilityBoard):
        if self._difficulty >= 2:
            maxValue = np.amax(probabilityBoard)
            for y, row in enumerate(probabilityBoard):
                for x, value in enumerate(row):
                    if value == maxValue:
                        print("AI attacked:",x,y)
                        return [x,y]
        elif self._difficulty == 1:
            sumOfDirections = sum(sum(probabilityBoard, []))
            toAttack = random.randint(0, sumOfDirections)
            count = 0
            for y, row in enumerate(probabilityBoard):
                for x, value in enumerate(row):
                    if count <= toAttack <= count + value:
                        print([x,y])
                        return [x,y]
                    count += value
                    
        print("DEBUG - AI Attacking Problem")

    def getAttack(self, ships, board):
        if self._hit is None:
            if self._difficulty < 3:
                print("normal attacking")
                probabilityBoard = [[0 for _ in range(len(board))] for _ in range(len(board[0]))]
                for ship in ships:
                    for yC in range(len(board)):
                        for xC in range(len(board[yC])):
                            probabilityBoard[yC][xC] += self.__validDirections(board, ship, xC, yC)
            else:
                sims = 10000
                probabilityBoard = [[0 for _ in range(10)] for _ in range (10)]
                taken = []
                for yi, y, in enumerate(board):
                    for xi, x in enumerate(y):
                        if x != 0:
                            taken.append([yi,xi])
                
                height = len(board)
                width = len(board[0])
                for _ in range(sims):
                    tempTaken = taken.copy()
                    for shipLength in ships:
                        direction = random.randint(0,3)
                        xC, yC = random.randrange(0,width), random.randrange(0,height)

                        if self.__isValid(direction, yC, xC, tempTaken, shipLength, width, height):
                            if direction == 0 or direction == 2:
                                if direction == 0:
                                    yC -= shipLength - 1
                                    for i in range(shipLength):
                                        probabilityBoard[yC+i][xC] += 1
                                        tempTaken.append([yC+i, xC])
                                        
                            if direction == 1 or direction == 3:
                                if direction == 3:
                                    xC -= shipLength - 1
                                for i in range(shipLength):
                                    probabilityBoard[yC][xC+i] += 1
                                    tempTaken.append([yC, xC+i])
            return self.__chooseAttackSquare(probabilityBoard)
        else:
            print("ortogonal strat")
            x = self._hit[0] + (self._hit[3] * self._directions[self._hit[2]][0])
            y = self._hit[1] + (self._hit[3] * self._directions[self._hit[2]][1])
            try:
                while board[y][x] == -1:
                    self._hit[3] += 1
                    x = self._hit[0] + (self._hit[3] * self._directions[self._hit[2]][0])
                    y = self._hit[1] + (self._hit[3] * self._directions[self._hit[2]][1])
            except IndexError:
                pass    

            print("AI attacked:",x,y)
            print(self._hit)
            print([x,y])
            return [x,y]

    def getShipPlacement(self, shipLength):
        board = self._board.getBoard()
        width = len(board[0])
        height = len(board)
        return f"{random.randrange(0, width)}{random.randrange(0, height)}{random.randrange(0, 2)}{shipLength}"

    def hitFeedback(self,result,x,y):
        print(result, self._hit)
        if self._hit is None and result == 1:
            self._hit = [x,y,0,1]
        elif self._hit is not None:
            if result == 1: # The orthogonal attack was a hit
                self._hit[3] += 1
            elif self._sides == 1:
                self._sides = 0 # The ship has been cleared out.
                self._hit = None
            elif result == -1: # it was a miss
                if self._hit[3] > 1: # We go to the other side of the ship/
                    self._hit[2] = (self._hit[2] + 2) % 4
                    self._hit[3] = 1
                    self._sides += 1
                else:
                    print("direction incremented")
                    self._hit[2] += 1 # Rotate direction 90 degrees clockwise.
            elif result == -2:
                print(self._hit)
                if self._hit[2] == 3:
                    self._hit = None
                else:
                    self._hit[2] += 1
