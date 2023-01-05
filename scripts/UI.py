from abc import abstractclassmethod
from cProfile import run
from tkinter import E
from Game import Game
from pprint import pprint as pp
import os
import pygame as pg
from art import *
from network import Network

class UI():
    def __init__(self):
        self._game = Game()
        self._username = "Guest" # This might be a problem.
        try:
            self._network = Network()
        except:
            print("Could not connect to server")

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
    def __options():
        raise NotImplementedError

    @abstractclassmethod
    def __networkGame():
        raise NotImplementedError

    @abstractclassmethod
    def __help():
        raise NotImplementedError

    @abstractclassmethod
    def __load():
        raise NotImplementedError

    #########################################################################
    #
    # CATEGORY A SKILL: HASHING
    # Using a hashing algorithm to securely transfer user passwords.
    #
    #########################################################################
    def hash(toHash):
        length = 100
        if len(toHash) >= length:
            return None
        else:
            while len(toHash)*2 <= 100:
                toHash += toHash
            toHash += toHash[:100-len(toHash)]
            print(len(toHash))

        prev = ord(toHash[0]) ^ ord(toHash[-1])
        new = chr(prev)
        for _ in range(1000):
            for ch in toHash[1:]:
                ch = ((ord(ch)^prev)%26)+65
                new += chr(((ch^prev) % 26) + 65)
                prev = (ch % 26) + 65
            toHash = new
            new = chr(prev)
        print("DEBUG -- hash complete")
        return toHash


class GUI(UI):
    def __init__(self):
        super().__init__()
        self._scale = 20
        self._width = 960
        self._height = 540
        self._finalImagePath = f"FinalImages\Scale{self._scale}\ "[:-1]

    def run(self):
        self.__menu()

    def __menu(self):
        # Initialise
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        running = True

        # Buttons
        rects = []
        buttonImages = [pg.image.load(f"{self._finalImagePath}LoginButton.png"), pg.image.load(f"{self._finalImagePath}SignUpButton.png"), pg.image.load(f"{self._finalImagePath}GuestButton.png"), pg.image.load(f"{self._finalImagePath}QuitButton.png")] 
        backgroundImage = pg.image.load(f"{self._finalImagePath}MainMenu.png") 
        for image in buttonImages:
            rects.append(image.get_rect())
        # Position buttons correctly.
        rects[0].update(int(round((5/96)*self._width)), int(round((19/54)*self._height)), rects[0].width, rects[0].height)
        rects[1].update(int(round((5/96)*self._width)), int(round((38/54)*self._height)), rects[1].width, rects[1].height)
        rects[2].update(int(round((53/96)*self._width)), int(round((19/54)*self._height)), rects[1].width, rects[2].height)
        rects[3].update(int(round((53/96)*self._width)), int(round((38/54)*self._height)), rects[1].width, rects[3].height)

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN: # Check if player pressed mouse
                    if event.button == 1: # Check if player pressed left mouse button
                        point = pg.mouse.get_pos() 
                        for i, rect in enumerate(rects):
                            if rect.collidepoint(point):
                                if i == 0:
                                    self.__logIn()
                                elif i == 1:
                                    self.__signUp()
                                elif i == 2:
                                    self.__playMenu()
                                else:
                                    running = False

            screen.blit(backgroundImage, (0,0))
            for image, rect in zip(buttonImages, rects):
                screen.blit(image, rect)

            pg.display.update()

    def __playMenu(self):
        # Initialise
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        running = True

        # Buttons
        rects = []
        buttonImages = [pg.image.load(f"{self._finalImagePath}Play.png"), pg.image.load(f"{self._finalImagePath}Help.png"), pg.image.load(f"{self._finalImagePath}Quit.png")] 
        backgroundImage = pg.image.load(f"{self._finalImagePath}MenuBackGround.png") 
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
                        for i, rect in enumerate(rects):
                            if rect.collidepoint(point):
                                pg.quit()
                                if i == 0:
                                    self.__local(False, 0)
                                elif i == 1:
                                    self.__local(True, 0)
                                elif i == 2:
                                    aiDifficulty = 2 #fix
                                    self.__local(False, aiDifficulty)
                                elif i == 3:
                                    self.__help()
                                elif i == 4:
                                    self.__options()
                                elif i == 5:
                                    self.__load()
                                else:
                                    running = False
                                    pg.quit()

            screen.blit(backgroundImage, (0,0))
            for x in range (len(rects)):
                screen.blit(buttonImages[x], rects[x])

            pg.display.update()

    def __local(self, network, ai, game=[Game(), True]): # Network is a boolean 
        if network:
            # Do the GUI version of this IMPORTANT FIX PROBLEM
            print(text2art("Online"))
            enemyName = input("What is your enemies username?")
            print("Setting up game with opponent...")
            playerNum, gameID = self._network.send(f"startGame {self._username} {enemyName}").split(" ")
            playerNum = int(playerNum[1]) - 1
            
        # Initialise
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        running = True
        currentPlayer = 0
        numships = 4 # change this to a get on the Game class.
        self._game = game[0]

        # Ships
        rects = []
        shipAttach = [0 for _ in range(numships)]
        shipImages = [pg.image.load(f"{self._finalImagePath}HP2Ship.png"), pg.image.load(f"{self._finalImagePath}HP3Ship.png"), pg.image.load(f"{self._finalImagePath}HP4Ship.png"), pg.image.load(f"{self._finalImagePath}HP5Ship.png")] 
        shipHP = [2,3,4,5]
        shipRotation = [0 for _ in range(numships)]
        shipLoc = [[(0, 0) for _ in range(numships)], [(0, 0) for _ in range(numships)]] # Stores the top and left coordinates of ships.
        for x in range(len(shipImages)):
            rects.append(shipImages[x].get_rect())

        # Buttons
        buttonImages = [pg.image.load(f"{self._finalImagePath}HP2Ship.png")]
        buttonRects = []
        for x in range(len(buttonImages)):
            buttonRects.append(buttonImages[x].get_rect())
        buttonRects[0].update(0, self._height-(2*buttonRects[0].height), buttonRects[0].width, buttonRects[0].height)

        # Grid
        WidthInSquares = 10 # Dimensions of the grid in squares.
        HeightInSquares = 10 
        squareSize = round(self._scale*2.5) 
        print(squareSize)
        # Edges of the grid
        left = self._width//2 - 5*squareSize   # Edges are five squares from the centre.
        right = self._width//2 + 5*squareSize
        top = self._height//2 - 5*squareSize
        bot = self._height//2 + 5*squareSize
        squares = []
        # Storing grid object in squares 
        for x in range(left, right, squareSize):
            for y in range(top, bot, squareSize):
                squares.append(pg.Rect(x, y, squareSize, squareSize))

        # Loop for placing ships
        if game[1]:
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
                        elif event.key == pg.K_o:
                            running = False # To skip to attacking for debugging. delete later
                        elif event.key == pg.K_d:
                            print(f"ShipAttach: {shipAttach}")
                            print(f"ShipHP: {shipHP}")
                            print(f"ShipImages: {shipImages}")
                            print(f"ShipLoc: {shipLoc}")
                            print(f"ShipRotation: {shipRotation}")
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1 and 1 not in shipAttach:
                            point = pg.mouse.get_pos()
                            if buttonRects[0].collidepoint(point) and 0 not in shipAttach and 1 not in shipAttach:  # buttonRects[0] is the done button
                                # place down all ships and swap turns (and move ships back) or move on to actual game.
                                for x in range(len(rects)):
                                    self._game.addShip(currentPlayer, f"{(rects[x].left - left)//squareSize}{(rects[x].top-top)//squareSize}{shipRotation[x]}{shipHP[x]}")
                                    shipLoc[currentPlayer][x] = [rects[x].left, rects[x].top]
                                    rects[x].update(0, 0, rects[x].width, rects[x].height) # Should probably also rotate these back to horizontal to not spoil IMPORTANT FIX PROBLEM
                                    print(f"ShipAttach: {shipAttach}") # IMPORTANT FIX PROBLEM
                                    print(f"ShipHP: {shipHP}")
                                    print(f"ShipImages: {shipImages}")
                                    print(f"ShipLoc: {shipLoc}")
                                    print(f"ShipRotation: {shipRotation}")
                                if currentPlayer == 0:
                                    currentPlayer = 1
                                    if ai != 0:
                                        for health in shipHP:
                                            self._game.addShip(1,self._game.getAIShip(health-2)) # health-2 = shipIndex
                                        running = False
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

                                    if shipRotation[x]:
                                        rects[x].update(squareSize * round((point[0] - (left % squareSize) - squareSize/2)/squareSize) + (left % squareSize), squareSize * round((point[1] - (top % squareSize) - shipHP[x]*squareSize/2)/squareSize) + (top % squareSize), rects[x].width, rects[x].height)
                                    else:
                                        rects[x].update(squareSize * round((point[0] - (left % squareSize) -  shipHP[x]*squareSize/2)/squareSize) + (left % squareSize), squareSize * round((point[1] - (top % squareSize) - squareSize/2)/squareSize) + (top % squareSize), rects[x].width, rects[x].height)
                                    
                                    break

                screen.fill((0,0,60))
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

            if network:
                board = self._game.getBoard(playerNum)
                grid = ""
                for y, row in enumerate(board):
                    for x, value in enumerate(row):
                        if value == 1:
                            grid += f"{x},{y}|"

                grid = grid[:-1]
                self._network.send(f"updateGrids {grid} {gameID} {playerNum}")
                enemyGrid = self._network.send(f"getGrid {gameID} {(playerNum+1)%2}").split("|")
                for coordinate in enemyGrid:
                    x,y = coordinate.split(",")
                    self._game.addShip((playerNum+1) % 2, f"{x}{y}11")


        # Attacking starts:

        currentPlayer = 0
        running = True
        shrinkScale = 1.15
        squareSize = int(squareSize//shrinkScale)  # Scale it down so that two grids can fit.
        # for x in shipImages:
        #     x = pg.image.load(f"FinImages\HP2Ship{self._scale/shrinkScale}.png")

        # Edges of the grids
        tempX = left
        tempY = top
        left = int(squareSize)
        right = int(2*left + WidthInSquares*squareSize*2)   # 2*left to leave a gap between the two grids.
        top = int(squareSize)
        bot = int(top + HeightInSquares*squareSize)
        squares = []
        enemySquares = []
        enemySecretBoard = []
        # Storing grid object in squares 
        for x in range(left, right//2, squareSize):
            for y in range(top, bot, squareSize):
                squares.append(pg.Rect(x, y, squareSize, squareSize))
        
        for x in range(right//2 + left, right, squareSize):
            for y in range(top, bot, squareSize):
                enemySquares.append(pg.Rect(x,y,squareSize,squareSize))

        attackTypePaths = [f"{self._finalImagePath}RegularAttack.png", f"{self._finalImagePath}Barrage.png", f"{self._finalImagePath}Radar.png"]
        attackType = 0
        attackTypeImage = pg.image.load(attackTypePaths[attackType])
        attackTypeRect = attackTypeImage.get_rect()
        attackTypeRect.update(1,1,1,1) # IMPORTANT PROBLEM FIX

        # Game loop   
        postHit = False         
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        postHit = False
                    elif event.key == pg.K_s:
                        self.__save() #IMPORTANT PROBLEM FIX -- Consider adding a check here, to make sure they want to save.
                        running = False
                    elif event.key == pg.K_c:
                        if attackTypeRect.collidepoint(point): 
                            # Change the attacktype
                            attackType = (attackType+1)%3
                            attackTypeImage = pg.image.load(attackTypePaths[attackType]) # IMPORTANT PROBLEM FIX
                            attackTypeRect = attackTypeImage.get_rect()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        point = pg.mouse.get_pos()
                        if attackTypeRect.collidepoint(point): 
                            # Change the attacktype
                            attackType = (attackType+1)%3
                            attackTypeImage = pg.image.load(attackTypePaths[attackType]) # IMPORTANT PROBLEM FIX
                            attackTypeRect = attackTypeImage.get_rect()
                        for x in range(len(enemySquares)):
                            if enemySquares[x].collidepoint(point): # Checks if the mouse is inside one of the grid squares.
                                # attack that square and swap sides
                                coords = [squareSize * round((point[0] - ((left + right//2 )% squareSize) - squareSize/2)/squareSize) + ((left + right//2) % squareSize), squareSize * round((point[1] - (top % squareSize) - squareSize/2)/squareSize) + (top % squareSize)]
                                coordinput = [(coords[0] - (left+right//2))//squareSize, (coords[1] - (top))//squareSize]
                                result = self._game.attack(coordinput[0], coordinput[1], (currentPlayer+1) % 2, attackType)
                                if result == 2:
                                    print(f"Print {currentPlayer} won!")
                                    running = False
                                elif result == 1:
                                    print("Hit!")
                                    pass
                                elif result == -1:
                                    print("Miss!")
                                    pass
                                postHit = True
                                if result == -2:
                                    # error or already attacked ship
                                    currentPlayer = (currentPlayer + 1) % 2 # Because we dont want to currentPlayer to remain the same in 2 lines.
                                    postHit = False

                                if network:
                                    previousAttack = self._network.send(f"updatePreviousAttack {coordinput[0]} {coordinput[1]} {playerNum} {attackType} {gameID}")
                                    print("Enemy player attacked - ", previousAttack) # IMPORTANT FIX PROBLEM 
                                    x, y, attackType, pnumignore = map(int, previousAttack.split(" "))
                                    self._game.attack(x, y, playerNum, attackType)

                                currentPlayer = (currentPlayer + 1) % 2
                                if currentPlayer == 1 and ai != 0:
                                    x,y = self._game.getAIAttack()
                                    self._game.attack(x,y,0,0)
                                    currentPlayer = (currentPlayer + 1) % 2
                                break # Nothing else to do if a square has been found to be attacked.
                                
            screen.fill((0,0,0))

            if not postHit:
                for x in range(len(rects)):
                    rects[x].update((shipLoc[currentPlayer][x][0]-(tempX-left))//shrinkScale, (shipLoc[currentPlayer][x][1]-(tempY-top))//shrinkScale, rects[x].width//shrinkScale, rects[x].height//shrinkScale)
                    screen.blit(shipImages[x], rects[x])

                mySecretBoard = self._game.getSBoard(currentPlayer)
                for x in range(len(squares)):
                    if mySecretBoard[x%10][x//10] >= 0:   # y coord is the % because of how I defined enemySquares.
                        pg.draw.rect(screen, (255,255,255), squares[x], 1) # White grid for an unknown
                    elif mySecretBoard[x%10][x//10] == -1:
                        pg.draw.rect(screen, (255,0,0), squares[x]) # Red fill for a hit ship
                    else:
                        pg.draw.rect(screen, (0,0,255), squares[x]) # Blue fill for known empty
                
                enemySecretBoard = self._game.getSBoard((currentPlayer+1)%2)  #0 = empty, -1 = hit ship, -2 = hit empty
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
            pg.display.update()

    def addNewResolution(self, newScale):
        scaleIncrease = newScale//2

        # Look into how you can read many image files from one folder.
        # IMPORTANT PORBLEM FIX
        pass

    def __help(self):
        # Initialise
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        running = True

        # Buttons
        help = pg.image.load(f"{self._finalImagePath}HelpScreen.png")

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            screen.blit(help, (0,0))
            pg.display.update()

    def __options(self): #IMPORTANT PROBLEM FIX
        changed = {}
        while True:
            ships = Game.getShips()
            width = Game.getWidth()
            height = Game.getHeight()
            numShips = [0,0,0,0,0,0]
            for ship in ships:
                numShips[ship-1] += 1
            specialsCounts = Game.getSpecials()
            numPlayers = Game.getNumPlayers()

            print("-----Options Menu-----")
            print(f"1. Grid Width {width}")
            print(f"2. Grid Height {height}")
            print(f"3. Ship One {numShips[0]}")
            print(f"4. Ship Two {numShips[1]}")
            print(f"5. Ship Three {numShips[2]}")
            print(f"6. Ship Four {numShips[3]}")
            print(f"7. Ship Five {numShips[4]}")
            print(f"8. Ship Six {numShips[5]}")

            print("-----Special Mode-----")
            print(f"9. Barrage {specialsCounts[0]}")
            print(f"10. Radar {specialsCounts[1]}")
            print(f"11. Mines {specialsCounts[2]}")
            print(f"12. Hit Streak {specialsCounts[3]}")
            print(f"13. Number of players {numPlayers}")
            print("")
            print("Write the number of the thing you want to change, followed by what it should be changed to. (e.g. 11 -1)")
            print("Write 'E' to exit")
            inp = input()
            toChange = inp.split(" ")[0]
            if toChange == "E":
                break
            newNum = inp.split(" ")[1]
            if newNum.isnumeric():
                newNum = int(newNum)
            else:
                continue
            changed[int(toChange)-1] = newNum

            if toChange == "1":
                Game.changeBoardDimensions(newNum, height)
            elif toChange == "2":
                Game.changeBoardDimensions(width, newNum)
            elif 3 <= int(toChange) <= 8:
                Game.changeShips(int(toChange) - 3, newNum)
            elif 9 <= int(toChange) <= 12:
                Game.changeSpecials(int(toChange)-9, newNum)
            elif toChange == "13":
                if newNum > 1:
                    Game.changeNumPlayers(newNum)
                else:
                    print("Must be 2 or more players")

        with open("options.txt", "r") as f:
            data = f.readlines()
        
        for index, newValue in changed.items():
            if index == 12:
                data[index] = str(newValue)
            else:
                data[index] = f"{newValue}\n"

        with open("options.txt", "w") as f:
            f.writelines(data)

    def __load(self): #IMPORTANT PROBLEM FIX
        if self._username is not None:
            loads = self._network.send(f"getLoads {self._username}")
        for load in loads.split(","):
            print(load)

        choice = input("Which game would you like to load?")
        grids = self._network.send(f"loadGame {choice}")
        grid1, grid2, ai = grids.split(" ")

        Game.changeAI(ai)
        game = Game()

        for coordinate in grid1.split("|"): 
            x,y = coordinate.split(",")
            game.addShip(0, f"{x}{y}{0}{1}")

        for coordinate in grid2.split("|"):
            x,y = coordinate.split(",")
            game.addShip(1, f"{x}{y}{0}{1}")

        self.__local(ai, [game, False])

    def __save(self): #IMPORTANT PROBLEM FIX
        if self._username is None:
            print("Must be logged in")
            return
        board1 = self._game.getBoard(0)
        grid1 = ""
        for y, row in enumerate(board1):
            for x, value in enumerate(row):
                if value == 1:
                    grid1 += f"{x},{y}|"
        grid1 = grid1[:-1]

        board2 = self._game.getBoard(1)
        grid2 = ""
        for y, row in enumerate(board2):
            for x, value in enumerate(row):
                if value == 1:
                    grid2 += f"{x},{y}|"
        grid2 = grid2[:-1]

        self._network.send(f'addGame {grid1} {grid2} {self._username} Guest ""')

    def __signUp(self):
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        running = True

        # Buttons
        rects = []
        buttonImages = [pg.image.load(f"{self._finalImagePath}Username.png"), pg.image.load(f"{self._finalImagePath}Password.png")]
        for image in buttonImages:
            rects.append(image.get_rect())
            rects[-1].update(int(round((350/960)*self._width)), int(round((190/540)*self._height)) + x*int(round((110/540)*self._height)), rects[-1].width, rects[-1].height) # repostion button
        backGround = pg.image.load(f"{self._finalImagePath}SignUpMenu.png")

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                # Figure out how to get text input from user, then make them input username, then password

            for index, image in enumerate(buttonImages):
                screen.blit(image, (rects[index].left, rects[index].top))
            screen.blit(backGround, (0,0))
            pg.display.update()

    def __logIn(self):
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        running = True

        # Buttons
        rects = []
        buttonImages = [pg.image.load(f"{self._finalImagePath}Username.png"), pg.image.load(f"{self._finalImagePath}Password.png")]
        for image in buttonImages:
            rects.append(image.get_rect())
            rects[-1].update(int(round((350/960)*self._width)), int(round((190/540)*self._height)) + x*int(round((110/540)*self._height)), rects[-1].width, rects[-1].height) # repostion button
        backGround = pg.image.load(f"{self._finalImagePath}SignUpMenu.png")

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                # Figure out how to get text input from user, then make them input username, then password

            for index, image in enumerate(buttonImages):
                screen.blit(image, (rects[index].left, rects[index].top))
            screen.blit(backGround, (0,0))
            pg.display.update()

class Terminal(UI):
    def __init__(self):
        super().__init__()
        
    def run(self):
        with open("options.txt", "r") as f:
            data = f.readline().split(",")
        print(data)
        data = list(map(int, data))
        Game.changeBoardDimensions(data[0], data[1])
        for index, numShips in enumerate(data[2:8]):
            Game.changeShips(index, numShips)
        for index, special in enumerate(data[8:12]):
            Game.changeSpecials(index, special)
        Game.changeNumPlayers(data[12])
        self.__mainMenu()
    
    def __mainMenu(self):
        while True:
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
                self.__playMenu()
            else:
                break

    def __signUp(self):
        valid = "not_unique"
        while valid == "not_unique":
            print("--The username must be unique--")
            self._username = input("Username - ")
            password = input("Password - ")
            if " " in self._username or " " in password:
                print("Username or password cannot have spaces!")
            else:
                valid = self._network.send(f"signUp {self._username} {self.hash(password + self._username)}")
            print("")
            
        self.__playMenu()

    def __logIn(self):
        valid = "false"
        while valid == "false":
            self._username = input("Username - ")
            password = input("Password - ")
            print("")
            valid = self._network.send(f"login {self._username} {self.hash(password + self._username)}")
        
        self.__playMenu()

    def __playMenu(self):
        while True:
            print(text2art("Battleships"))
            print("1. Local")
            print("2. Network")
            print("3. AI Opponent")
            print("4. Help")
            print("5. Options")
            print("6. Load Game")
            print("7. Quit")
            opt = input()
            if opt == "1":
                self.__local(0) # No ai
            elif opt == "2":
                self.__networkGame()
            elif opt == "3":
                self.__local(input("What AI difficulty? 1,2 or 3"))
            elif opt == "4":
                self.__help()
            elif opt == "5":
                self.__options()
            elif opt == "6":
                self.__load()
            else:
                break
   
    def __getShipInput(self, playerNumber, ai, y): # x = player number, ai = ai difficulty, y = index of ship to be placed
        if int(ai) != 0:
            if playerNumber == 1:
                return self._game.getAIShip(y)
        return input((f"Ship in format xyr"))

    def __getAttackInput(self, playerNumber, ai): # x = player number, ai = ai difficulty
        if int(ai) != 0:
            if playerNumber == 1:
                return self._game.getAIAttack(), 0
        print("Your specials: [barrageCount, radarCount]")
        print(self._game.getSpecialCount(playerNumber)[:-2]) # Don't care about mines or hitstreak
        print("0 - normal, 1 - barrage, 2 - radar")
        attackType = int(input("What attack do you want to use?"))
        if attackType <= 1:
            coordinates = input("Input square to attack (x,y), can't attack the same square twice.").split(",")
            return coordinates, attackType
        return 0, attackType

    def __local(self,aiDifficulty, game=[Game(), True]): # aiDifficulty is 0,1,2 or 3, 0 for no ai, and then 1,2,3 for difficulty level.
        Game.changeAI(aiDifficulty)
        print("AI difficulty:", aiDifficulty)
        self._game = game[0]
        numPlayers = Game.getNumPlayers()

        if game[1]:
            for playerNum in range(numPlayers): # Placing ships.
                print(f"Player {playerNum+1} turn")
                pp(self._game.getBoard(playerNum))

                numShips = Game.getNumShips()
                ships = Game.getShips()

                for ship in ships:
                    print(f"Player {playerNum+1} to place down ship of length {ship}")
                    while self._game.addShip(playerNum, f"{self.__getShipInput(playerNum, aiDifficulty, numShips-1)}{ship}") == -1:
                        print("Invalid ship position, current state of board:")
                        pp(self._game.getBoard(playerNum))
                    numShips -= 1

                pp(self._game.getBoard(playerNum))

                input("Press enter to change turns and clear terminal")
                os.system('cls')

            print("Time to attack!")
        play = True
        while play:
            choice = input("Write 's' to save, anything else to continue")
            if choice.lower() == "s":
                if numPlayers != 2:
                    print("Can only save two player games.") # IMPORANT FIX PROBLEM
                self.__save()
                break
            for playerNum in range(numPlayers):
                print(f"Player {playerNum+1} turn")
                print(f"Player {playerNum+1} board:")
                pp(self._game.getBoard(playerNum))
                for deltaPlayer in range(1, numPlayers):

                    print(f"Player {((playerNum+deltaPlayer) % numPlayers) + 1} secret board:")
                    for row in self._game.getSBoard((playerNum+deltaPlayer) % numPlayers): # it returns a 2d array, so we print the rows.
                        print(row)

                    result = -2
                    while result == -2: # Returing -2 = already hit square or error, -1 = miss, 1 = hit ship, 2 = game won
                        attackLocation, attackType = self.__getAttackInput(playerNum, aiDifficulty)
                        result = -2
                        if attackType == 2:
                            result = self._game.radar((playerNum+deltaPlayer) % numPlayers)
                            print(f"There is a ship at x={result[0]}, y={result[1]}")
                        else:
                            try:
                                result = self._game.attack(int(attackLocation[0]), int(attackLocation[1]), (playerNum+deltaPlayer) % numPlayers, attackType) # Index starts at 0
                            except IndexError:
                                print("Invalid attack format")
                    if result == 2:
                        print("Hit!")
                        print(f"Player {playerNum+1} wins!")
                        play = False
                    elif result == 1:
                        print("Hit!")
                    elif result == -1:
                        print("Miss!")

                input("Press enter to change turns and clear terminal")
                os.system('cls')

    def __networkGame(self, game=[Game(), True]):
        self._game = game[0]
        if game[1]:
            if self._username == "Guest":
                print("Must be logged in!")
                return
            print(text2art("Online"))
            enemyName = input("What is your enemy's username?")
            print("Setting up game with opponent...")
            playerNum, gameID = self._network.send(f"startGame {self._username} {enemyName}").split(" ")
            playerNum = int(playerNum[1]) - 1

            # get and compare player statistics
            myStats = self._network.send(f"getStats {self._username}") # s1|s2|s3|s4
            enemyStats = self._network.send(f"getStats {enemyStats}")
            needsHelp = self._compare(myStats, enemyStats)
            if needsHelp != -1:
                print(f"It is recommended that player {needsHelp+1} gets help Y/N")
                if needsHelp == playerNum:
                    if input("Do you want to change your options to make the game easier? (Y/N)").upper() == "Y":
                        self.__options()
                    else:
                        print("OK, continue as is. Good luck!")
                else:
                    print("Checking if enemy player wants to get help.")

            pp(self._game.getBoard(playerNum))
            numShips = Game.getNumShips()
            ships = Game.getShips()

            for ship in ships:
                print(f"Place down a ship of length {ship}")
                while self._game.addShip(playerNum, f"{self.__getShipInput(playerNum, 0, numShips-1)}{ship}") == -1:
                    print("Invalid ship position, current state of board:")
                    pp(self._game.getBoard(playerNum))
                    numShips += 1
                numShips -= 1

            board = self._game.getBoard(playerNum)
            grid = ""
            for y, row in enumerate(board):
                for x, value in enumerate(row):
                    if value == 1:
                        grid += f"{x},{y}|"

            grid = grid[:-1]
            self._network.send(f"updateGrids {grid} {gameID} {playerNum}")
            enemyGrid = self._network.send(f"getGrid {gameID} {(playerNum+1)%2}").split("|")
            for coordinate in enemyGrid:
                x,y = coordinate.split(",")
                self._game.addShip((playerNum+1) % 2, f"{x}{y}11")
        # Ships have been placed
        # Start attacking:

        play = True
        while play:
            print("Your board:")
            pp(self._game.getBoard(playerNum))
            print("")
            print("Enemy secret board")
            pp(self._game.getSBoard((playerNum+1)%2))
            result = -2
            while result == -2: # Returing -2 = already hit square or error, -1 = miss, 1 = hit ship, 2 = game won
                attackLocation, attackType = self.__getAttackInput(playerNum, 0)
                result = -2
                if attackType == 2:
                    result = self._game.radar((playerNum+1) % 2)
                    print(f"There is a ship at x={result[0]}, y={result[1]}")
                else:
                    try:
                        result = self._game.attack(int(attackLocation[0]), int(attackLocation[1]), (playerNum+1) % 2, attackType) # Index starts at 0
                    except IndexError:
                        print("Invalid attack format")
            if result == 2:
                print("Hit!")
                print(f"Player {playerNum+1} wins!")
                play = False
                self._network.send(f"won {playerNum}")
            elif result == 1:
                print("Hit!")
            elif result == -1:
                print("Miss!")
            
            previousAttack = self._network.send(f"updatePreviousAttack {attackLocation[0]} {attackLocation[1]} {playerNum} {attackType} {gameID}")
            print("Enemy player attacked - ", previousAttack)
            x, y, attackType, pnumignore = map(int, previousAttack.split(" "))
            self._game.attack(x, y, playerNum, attackType)

    def __help(self):
        print("\n")
        print(text2art("RULES"))
        print("The game consists of consists of two phases, the preparation and attack phases.")
        print("In the preperation phase, players place own all of their ships on a grid (often 10x10).")
        print("---------------------------------------------------------------------------------------")
        print("In the attack phase, it is time to attack the other players' ships")
        print("Do this by choosing a square on the grid that you think contains an enemy ship")
        print("You will be told whether your attack was a hit, then it changes to another players turn")
        print("---------------------------------------------------------------------------------------")
        print("This cycle continues until one player has destroyed all of the enemies ships.")
        print("The last player with ships remaining wins!")
        input("Press any button to continue.")

    def __options(self):
        changed = {}
        while True:
            ships = Game.getShips()
            width = Game.getWidth()
            height = Game.getHeight()
            numShips = [0,0,0,0,0,0]
            for ship in ships:
                numShips[ship-1] += 1
            specialsCounts = Game.getSpecials()
            numPlayers = Game.getNumPlayers()

            print("-----Options Menu-----")
            print(f"1. Grid Width {width}")
            print(f"2. Grid Height {height}")
            print(f"3. Ship One {numShips[0]}")
            print(f"4. Ship Two {numShips[1]}")
            print(f"5. Ship Three {numShips[2]}")
            print(f"6. Ship Four {numShips[3]}")
            print(f"7. Ship Five {numShips[4]}")
            print(f"8. Ship Six {numShips[5]}")

            print("-----Special Mode-----")
            print(f"9. Barrage {specialsCounts[0]}")
            print(f"10. Radar {specialsCounts[1]}")
            print(f"11. Mines {specialsCounts[2]}")
            print(f"12. Hit Streak {specialsCounts[3]}")
            print(f"13. Number of players {numPlayers}")
            print("")
            print("Write the number of the thing you want to change, followed by what it should be changed to. (e.g. 11 -1)")
            print("Write 'E' to exit")
            inp = input()
            toChange = inp.split(" ")[0]
            if toChange == "E":
                break
            newNum = inp.split(" ")[1]
            if newNum.isnumeric():
                newNum = int(newNum)
            else:
                continue
            changed[int(toChange)-1] = newNum

            if toChange == "1":
                Game.changeBoardDimensions(newNum, height)
            elif toChange == "2":
                Game.changeBoardDimensions(width, newNum)
            elif 3 <= int(toChange) <= 8:
                Game.changeShips(int(toChange) - 3, newNum)
            elif 9 <= int(toChange) <= 12:
                Game.changeSpecials(int(toChange)-9, newNum)
            elif toChange == "13":
                if newNum > 1:
                    Game.changeNumPlayers(newNum)
                else:
                    print("Must be 2 or more players")

        with open("options.txt", "r") as f:
            data = f.readlines()
        
        for index, newValue in changed.items():
            if index == 12:
                data[index] = str(newValue)
            else:
                data[index] = f"{newValue}\n"

        with open("options.txt", "w") as f:
            f.writelines(data)

    def __load(self):
        if self._username is not None:
            loads = self._network.send(f"getLoads {self._username}")
        for load in loads.split(","):
            print(load)

        choice = input("Which game would you like to load?")
        grids = self._network.send(f"loadGame {choice}")
        grid1, grid2, ai = grids.split(" ")

        Game.changeAI(ai)
        game = Game()

        for coordinate in grid1.split("|"): 
            x,y = coordinate.split(",")
            game.addShip(0, f"{x}{y}{0}{1}")

        for coordinate in grid2.split("|"):
            x,y = coordinate.split(",")
            game.addShip(1, f"{x}{y}{0}{1}")

        self.__local(ai, [game, False])

    def __save(self):
        if self._username is None:
            print("Must be logged in")
            return
        board1 = self._game.getBoard(0)
        grid1 = ""
        for y, row in enumerate(board1):
            for x, value in enumerate(row):
                if value == 1:
                    grid1 += f"{x},{y}|"
        grid1 = grid1[:-1]

        board2 = self._game.getBoard(1)
        grid2 = ""
        for y, row in enumerate(board2):
            for x, value in enumerate(row):
                if value == 1:
                    grid2 += f"{x},{y}|"
        grid2 = grid2[:-1]

        self._network.send(f'addGame {grid1} {grid2} {self._username} Guest ""')