from abc import abstractclassmethod
from Game import Game
from pprint import pprint as pp
import os
import pygame as pg
from art import *


class UI():
    def __init__(self):
        self._game = Game()
        self._numShips = 4

    @abstractclassmethod
    def __run():
        raise NotImplementedError

    @abstractclassmethod
    def __local():
        raise NotImplementedError

    @abstractclassmethod
    def __signUp():
        raise NotImplementedError

    @abstractclassmethod
    def __logIn():
        raise NotImplementedError

    @abstractclassmethod
    def __help():
        raise NotImplementedError

class GUI(UI):
    def __init__(self):
        super().__init__()
        self._scale = 2.0
        self._width = 960
        self._height = 540

    def run(self):
        self.__menu()

    def __menu(self):
        # Initialise
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        running = True

        # Buttons
        rects = []
        buttonImages = [pg.image.load(f"FinImages\Play{self._scale}.png"), pg.image.load(f"FinImages\Help{self._scale}.png"), pg.image.load(f"FinImages\Quit{self._scale}.png")] 
        bgImage = pg.image.load(f"FinImages\MenuBackGround{self._scale}.png") 
        for x in range(len(buttonImages)):
            rects.append(buttonImages[x].get_rect())
            rects[x].update(int(round((350/960)*self._width)), int(round((190/540)*self._height)) + x*int(round((110/540)*self._height)), rects[x].width, rects[x].height)

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Check which menu button it collided with and call that function.
                        point = pg.mouse.get_pos()
                        for x in range(len(rects)):
                            if rects[x].collidepoint(point):
                                pg.quit()
                                if x == 0:
                                    self.__playMenu()
                                elif x == 1:
                                    self.__help()
                                else:
                                    running = False
                                    pg.quit()

            screen.blit(bgImage, (0,0))
            for x in range (len(rects)):
                screen.blit(buttonImages[x], rects[x])

            pg.display.update()

    def __playMenu(self):
        self.__local()

    def __local(self):
        # Initialise
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        running = True
        currPlayer = 0

        # Ships
        rects = []
        shipAttach = [0, 0, 0]
        shipImages = [pg.image.load(f"FinImages\HP2Ship{self._scale}.png"), pg.image.load(f"FinImages\HP2Ship{self._scale}.png"), pg.image.load(f"FinImages\HP2Ship{self._scale}.png")] 
        shipHP = [2, 2, 2, 2]
        shipRotation = [0, 0, 0]
        shipLoc = [[[0, 0] for _ in range(len(shipAttach))], [[0,0] for _ in range(len(shipAttach))]] # Stores the top and left coordinates of ships.
        for x in range(len(shipImages)):
            rects.append(shipImages[x].get_rect())
            #scale these correctly, each square is 40*40 pixels.

        # Buttons
        buttonImages = [pg.image.load(f"FinImages\HP2Ship{self._scale}.png")]
        buttonRects = []
        for x in range(len(buttonImages)):
            buttonRects.append(buttonImages[x].get_rect())
        buttonRects[0].update(0, self._height-(2*buttonRects[0].height), buttonRects[0].width, buttonRects[0].height)

        # Grid
        WidthInSquares = 10 # Dimensions of the grid in squares.
        HeightInSquares = 10 
        squareSize = self._height//(HeightInSquares+1) # +1 to give a little bit of space.
        # Edges of the grid
        xLeft = self._width//2 - 5*squareSize   # Edges are five squares from the centre.
        xRight = self._width//2 + 5*squareSize
        yTop = self._height//2 - 5*squareSize
        yBot = self._height//2 + 5*squareSize
        squares = []
        # Storing grid object in squares 
        for x in range(xLeft, xRight, squareSize):
            for y in range(yTop, yBot, squareSize):
                squares.append(pg.Rect(x, y, squareSize, squareSize))

        # Loop for placing ships
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_r: 
                        for x in range(len(shipAttach)):
                            if shipAttach[x] == 1:
                                if shipRotation[x]:
                                    shipRotation[x] = 0
                                else:
                                    shipRotation[x] = 1
                                shipImages[x] = pg.transform.rotate(shipImages[x], -90)
                                rects[x] = shipImages[x].get_rect()
                                break
                    if event.key == pg.K_o:
                        running = False # To skip to attacking for debugging. delete later
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1 and 1 not in shipAttach:
                        point = pg.mouse.get_pos()
                        if buttonRects[0].collidepoint(point) and 0 not in shipAttach and 1 not in shipAttach:  # buttonRects[0] is the done button
                            # place down all ships and swap turns (and move ships back) or move on to actual game.
                            for x in range(len(rects)):
                                self._game.addShip(currPlayer, f"{(rects[x].left - xLeft)//squareSize}{(rects[x].top-yTop)//squareSize}{shipRotation[x]}{shipHP[x]}")
                                shipLoc[currPlayer][x] = [rects[x].left, rects[x].top]
                                rects[x].update(0, 0, rects[x].width, rects[x].height) # Should probably also rotate these back to horizontal to not spoil
                            if currPlayer == 0:
                                currPlayer = 1
                            else:
                                running = False
                            
                        for x in range(len(rects)):
                            if rects[x].collidepoint(point): # Checks if the mouse is inside one of the ships.
                                # Mouse attaches to ship and starts moving it around.
                                shipAttach[x] = 1
                                break  # Break cause otherwise you can pick up multiple ships at once.
                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1 and 1 in shipAttach:
                        point = pg.mouse.get_pos()
                        for x in range(len(shipAttach)):
                            if shipAttach[x] == 1: # If the ship is currently being held, place it down.
                                shipAttach[x] = 2

                                # An issue with this line: the (point[a] - squaresize/2) depends on the ships HP and its rotation (e.g. how much u minus depends.)
                                if shipRotation[x]:
                                    rects[x].update(squareSize * round((point[0] - (xLeft % squareSize) - squareSize/2)/squareSize) + (xLeft % squareSize), squareSize * round((point[1] - (yTop % squareSize) - shipHP[x]*squareSize/2)/squareSize) + (yTop % squareSize), rects[x].width, rects[x].height)
                                else:
                                    rects[x].update(squareSize * round((point[0] - (xLeft % squareSize) -  shipHP[x]*squareSize/2)/squareSize) + (xLeft % squareSize), squareSize * round((point[1] - (yTop % squareSize) - squareSize/2)/squareSize) + (yTop % squareSize), rects[x].width, rects[x].height)
                                
                                # self._game.addShip(currPlayer, f"{(rects[x].left - xLeft)//squareSize}{(rects[x].top-yTop)//squareSize}{shipRotation[x]}{shipHP[x]}")
                                # Move the above line to something that comes after the user has press a "done" button
                                break

            screen.fill((0,0,0))
            for x in range(len(shipAttach)):  # Makes a ship follow the mouse around once it has been clicked.
                if shipAttach[x] == 1:
                    rects[x].update(pg.mouse.get_pos()[0] - rects[x].width/2, pg.mouse.get_pos()[1] - rects[x].height/2, rects[x].width, rects[x].height)

            for square in squares:
                pg.draw.rect(screen, (255,255,255), square, 1)

            for x in range (len(rects)):
                screen.blit(shipImages[x], rects[x])

            for x in range(len(buttonImages)):
                screen.blit(buttonImages[x], buttonRects[x])

            pg.display.update()


        # Attacking starts:

        currPlayer = 0
        running = True
        shrinkScale = 1.15
        squareSize = int(squareSize//shrinkScale)  # Scale it down so that two grids can fit.
        # for x in shipImages:
        #     x = pg.image.load(f"FinImages\HP2Ship{self._scale/shrinkScale}.png")

        # Edges of the grids
        tempX = xLeft
        tempY = yTop
        xLeft = int(squareSize)
        xRight = int(2*xLeft + WidthInSquares*squareSize*2)   # 2*xLeft to leave a gap between the two grids.
        yTop = int(squareSize)
        yBot = int(yTop + HeightInSquares*squareSize)
        squares = []
        enemySquares = []
        enemySecretBoard = []
        # Storing grid object in squares 
        for x in range(xLeft, xRight//2, squareSize):
            for y in range(yTop, yBot, squareSize):
                squares.append(pg.Rect(x, y, squareSize, squareSize))
        
        for x in range(xRight//2 + xLeft, xRight, squareSize):
            for y in range(yTop, yBot, squareSize):
                enemySquares.append(pg.Rect(x,y,squareSize,squareSize))

        # Game loop   
        postHit = False         
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    if event.type == pg.K_a:
                        postHit = False
                        print("a")
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        point = pg.mouse.get_pos()
                        for x in range(len(enemySquares)):
                            if enemySquares[x].collidepoint(point): # Checks if the mouse is inside one of the grid squares.
                                # attack that square and swap sides
                                coords = [squareSize * round((point[0] - ((xLeft + xRight//2 )% squareSize) - squareSize/2)/squareSize) + ((xLeft + xRight//2) % squareSize), squareSize * round((point[1] - (yTop % squareSize) - squareSize/2)/squareSize) + (yTop % squareSize)]
                                coordinput = [(coords[0] - (xLeft+xRight//2))//squareSize, (coords[1] - (yTop))//squareSize]
                                result = self._game.attack(coordinput[0], coordinput[1], (currPlayer+1) % 2)
                                if result == 2:
                                    # a hit and currPlayer won
                                    running = False
                                elif result == 1:
                                    # a hit
                                    pass
                                elif result == -1:
                                    # a miss
                                    pass
                                elif result == -2:
                                    # error or already attacked ship
                                    currPlayer = (currPlayer + 1) % 2 # Because we dont want to currPlayer to remain the same in 2 lines.
                                postHit = True
                                currPlayer = (currPlayer + 1) % 2
                                break # Nothing else to do if a square has been found to be attacked.
                                

            screen.fill((0,0,0))

            if not postHit:
                for x in range(len(rects)):
                    rects[x].update((shipLoc[currPlayer][x][0]-(tempX-xLeft))//shrinkScale, (shipLoc[currPlayer][x][1]-(tempY-yTop))//shrinkScale, rects[x].width//shrinkScale, rects[x].height//shrinkScale)
                    screen.blit(shipImages[x], rects[x])

                mySecretBoard = self._game.getSBoard(currPlayer)
                for x in range(len(squares)):
                    if mySecretBoard[x%10][x//10] >= 0:   # y coord is the % because of how I defined enemySquares.
                        pg.draw.rect(screen, (255,255,255), squares[x], 1) # White grid for an unknown
                    elif mySecretBoard[x%10][x//10] == -1:
                        pg.draw.rect(screen, (255,0,0), squares[x]) # Red fill for a hit ship
                    else:
                        pg.draw.rect(screen, (0,0,255), squares[x]) # Blue fill for known empty
                
                enemySecretBoard = self._game.getSBoard((currPlayer+1)%2)  #0 = empty, -1 = hit ship, -2 = hit empty
                for x in range(len(enemySquares)):
                    if enemySecretBoard[x%10][x//10] >= 0:   # y coord is the % because of how I defined enemySquares.
                        pg.draw.rect(screen, (255,255,255), enemySquares[x], 1) # White grid for an unknown
                    elif enemySecretBoard[x%10][x//10] == -1:
                        pg.draw.rect(screen, (255,0,0), enemySquares[x]) # Red fill for a hit ship
                    else:
                        pg.draw.rect(screen, (0,0,255), enemySquares[x]) # Blue fill for known empty
            else:
                # Display the hitting animation, or a "press space to resume screen."
                pass
            print(1)
            pg.display.update()

    def __help(self):
        pass

    def __signUp(self):
        pass

    def __logIn(self):
        pass

class Terminal(UI):
    def __init__(self):
        super().__init__()

    def run(self):
        print(text2art("Battleships"))
        print("Main Menu:")
        print("1. Log in")
        print("2. Sign up")
        print("3. Guest")
        print("4. Quit")

        opt = input()
        if opt == "1":
            self.__logIn()
        elif opt == "2":
            self.__signUp()
        elif opt == "3":
            self.__local()
    
    def __local(self):
        for x in range(2):
            print(f"Player {x+1} turn")
            pp(self._game.getBoard(x))
            y = self._numShips
            while y > 0:
                if self._game.addShip(x, input((f"{y} Ships in format xyrh"))) == -1:
                    print("Invalid ship position, current state of board:")
                    pp(self._game.getBoard(x))
                    y += 1
                y -= 1
            pp(self._game.getBoard(x))
            input("Press enter to change turns and clear terminal")
            os.system('cls||clear')

        print("Time to attack!")
        play = True
        while play:
            for x in range(2):
                print(f"Player {x+1} turn")
                print(f"Player {x+1} board:")
                pp(self._game.getBoard(x))

                print(f"Player {((x+1)%2)+1} secret board:")
                for y in self._game.getSBoard((x+1)%2): # it retruns a 2d array, so we print the rows.
                    print(y)

                while True:
                    result = -2
                    while result == -2: # Returing -2 = already hit square or error, -1 = miss, 1 = hit ship, 2 = game won
                        attack = input("Input square to attack (xy), can't attack the same square twice.")
                        result = -2
                        result = self._game.attack(int(attack[0]), int(attack[1]), (x+1)%2) # Index starts at 0
                    if result == 2:
                        print("Hit!")
                        print(f"Player {x+1} wins!")
                        play = False
                        break
                    elif result == 1:
                        print("Hit!")
                    elif result == -1:
                        print("Miss!")
                    input("Press enter to change turns and clear terminal")
                os.system('cls||clear')

    def __signUp():
        pass

    def __logIn():
        pass

    def __help():
        pass
