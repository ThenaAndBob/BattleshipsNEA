from abc import abstractclassmethod
from cProfile import run
from tkinter import E
from Game import Game
from pprint import pprint as pp
import os
import random
import pygame as pg
from art import *
from network import Network
from PIL import Image
import time

class UI():
    def __init__(self):
        self._username = "" 
        try:
            self._network = Network()
            pass
        except:
            print("Could not connect to server")

    @abstractclassmethod
    def __run():
        raise NotImplementedError

    @abstractclassmethod
    def __local():
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

    @abstractclassmethod
    def __save():
        raise NotImplementedError
        
    #########################################################################
    #
    # CATEGORY A SKILL: HASHING
    # Using a hashing algorithm to securely transfer user passwords.
    #
    #########################################################################
    def hash(self, toHash):
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

    def compareStats(self, s1, s2): # wins,losses,hits,misses,highestHP,leastAttacks
        s1 = list(map(int, s1))
        s2 = list(map(int, s2))

        winrate1 = s1[0]/(s1[0]+s1[1])
        hitrate1 = s1[2]/(s1[2]+s1[3])

        winrate2 = s2[0]/(s2[0]+s2[1])
        hitrate2 = s2[2]/(s2[2]+s2[3])

        if abs(winrate1-winrate2) > 0.1:
            if winrate1 < winrate2:
                return 0
            else:
                return 1
        if abs(hitrate1-hitrate2) > 0.1:
            if hitrate1 < hitrate2:
                return 0
            else:
                return 1
        return -1

class GUI(UI):
    def __init__(self):
        super().__init__()
        self._scale = 20
        self._width = 960
        self._height = 540
        self._finalImagePath = f"FinalImages\\Scale{self._scale}\\"

    def run(self):
        with open("options.txt", "r") as f:
            data = f.readline()
            data = data.split(",")
        data = list(map(int, data))
        Game.changeBoardDimensions(data[0], data[1])
        for index, number in enumerate(data[2:8]):
            Game.changeShips(index, number)
        for index, number in enumerate(data[8:13]):
            Game.changeSpecials(index, number)
        Game.changeNumPlayers(data[13])

        self.__mainMenu()

    def __mainMenu(self):
        # Initialise
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        runningMenu = True

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

        while runningMenu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    runningMenu = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        runningMenu = False
                elif event.type == pg.MOUSEBUTTONDOWN: # Check if player pressed mouse
                    if event.button == 1: # Check if player pressed left mouse button
                        point = pg.mouse.get_pos() 
                        for i, rect in enumerate(rects):
                            if rect.collidepoint(point):
                                if i == 0:
                                    self.__authenticate("login")
                                elif i == 1:
                                    self.__authenticate("signup")
                                elif i == 2:
                                    self.__playMenu()
                                else:
                                    runningMenu = False

            screen.blit(backgroundImage, (0,0))
            for image, rect in zip(buttonImages, rects):
                screen.blit(image, rect)

            pg.display.update()

    def __playMenu(self):
        # Initialise
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        runningPlayMenu = True

        # Buttons
        rects = [None for _ in range(7)]
        backgroundImagePlayMenu = pg.image.load(f"{self._finalImagePath}playMenu.png") 
        rects[0] = pg.Rect(3*self._scale, 11*self._scale, 19*self._scale, 5*self._scale)
        rects[1] = pg.Rect(24*self._scale,11*self._scale,21*self._scale,5*self._scale)
        rects[2] = pg.Rect(3*self._scale, 18*self._scale, 5*self._scale, 5*self._scale)
        rects[3] = pg.Rect(37*self._scale,20*self._scale,3*self._scale,5*self._scale)
        rects[4] = pg.Rect(31*self._scale,20*self._scale,5*self._scale,5*self._scale)
        rects[5] = pg.Rect(12*self._scale,18*self._scale,15*self._scale,5*self._scale)
        rects[6] = pg.Rect(41*self._scale,20*self._scale,5*self._scale,5*self._scale)

        while runningPlayMenu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    runningPlayMenu = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        runningPlayMenu = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Check which menu button it collided with and call that function.
                        point = pg.mouse.get_pos()
                        for i, rect in enumerate(rects):
                            if rect.collidepoint(point):
                                if i == 0:
                                    self.__local(False, 0)
                                elif i == 1:
                                    self.__local(True, 0)
                                elif i == 2:
                                    aiDifficulty = self.__getUserInput("aidifficulty")
                                    try:
                                        aiDifficulty = int(aiDifficulty)
                                    except ValueError:
                                        break
                                    Game.changeAI(aiDifficulty)
                                    self.__local(False, aiDifficulty)
                                elif i == 3:
                                    self.__help()
                                elif i == 4:
                                    self.__options()
                                elif i == 5:
                                    self.__load()
                                else:
                                    runningPlayMenu = False
                                    pg.quit()
            screen.blit(backgroundImagePlayMenu, (0,0))
            pg.display.update()

    def __local(self, network, ai, game=None): # Network is a boolean             
        # Initialise
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        runningLocal = True
        currentPlayer = 0

        numships = Game.getNumShips()
        if game is None:
            self._game = Game()
            numPlayers = Game.getNumPlayers()
        else:
            self._game = game[0]
            numPlayers = 2

        if network:
            enemyName = self.__getUserInput("EnemyName")
            playerNum, gameID = self._network.send(f"startGame {self._username} {enemyName}").split(" ")
            playerNum = int(playerNum[1]) - 1
            numPlayers = 1

        # Ships
        rects = []
        shipAttach = [0 for _ in range(numships)]
        shipImages = []
        shipHP = Game.getShips()
        for ship in shipHP:
            shipImages.append(pg.image.load(f"{self._finalImagePath}HP{ship}Ship.png"))
        shipRotation = [0 for _ in range(numships)]
        for image in shipImages:
            rects.append(image.get_rect())

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
        
        playerNumberImage = [pg.image.load(f"{self._finalImagePath}P.png"), pg.image.load(f"{self._finalImagePath}{currentPlayer+1}.png")]

        # Loop for placing ships
        if game is None:
            while runningLocal:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        runningLocal = False
                        if network:
                             self._network.send(f"deletegame {gameID}")
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
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1 and 1 not in shipAttach:
                            point = pg.mouse.get_pos()
                            changePlayer = True
                            if buttonRects[0].collidepoint(point) and 0 not in shipAttach and 1 not in shipAttach:  # buttonRects[0] is the done button
                                # place down all ships and swap turns (and move ships back) or move on to actual game.
                                for x in range(len(rects)):
                                    shipResult = self._game.addShip(currentPlayer, f"{(rects[x].left - left)//squareSize}{(rects[x].top-top)//squareSize}{shipRotation[x]}{shipHP[x]}")
                                    if shipRotation[x]:
                                        shipImages[x] = pg.transform.rotate(shipImages[x], -90)
                                        rects[x] = shipImages[x].get_rect()
                                        shipRotation[x] = 0
                                    rects[x].update(0, 0, rects[x].width, rects[x].height) 
                                    if shipResult == -1:
                                        changePlayer = False
                                
                                print(currentPlayer, numPlayers)
                                if changePlayer:
                                    if currentPlayer == 0:
                                        if ai != 0:
                                            for health in shipHP:
                                                self._game.addShip(1,self._game.getAIShip(health-2)) # health-2 = shipIndex
                                            runningLocal = False
                                    if currentPlayer == numPlayers-1:
                                        runningLocal = False
                                    currentPlayer += 1
                                    playerNumberImage[1] = pg.image.load(f"{self._finalImagePath}{currentPlayer+1}.png")
                                else:
                                    self._game.clearBoard(currentPlayer)

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

                P, pn = playerNumberImage
                screen.blit(P, (round(screen.get_width()-(6*self._scale)), 0))
                screen.blit(pn, (round(screen.get_width()-(3*self._scale)), 0))
                pg.display.update()

            if network:
                board = self._game.getBoard(0)
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
                    self._game.addShip(1, f"{x}{y}11")

        # Attacking starts:
        currentPlayer = 0
        playerNumbers = [num for num in range(numPlayers)]
        runningLocal = True
        shrinkScale = 1.15
        squareSize = int(squareSize//shrinkScale)  # Scale it down so that two grids can fit.
        numAttacked = 0

        # Edges of the grids
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

        attackTypePaths = [f"{self._finalImagePath}N.png", f"{self._finalImagePath}B.png", f"{self._finalImagePath}R.png"]
        attackType = 0
        attackTypeImage = pg.image.load(attackTypePaths[attackType])
        attackTypeRect = attackTypeImage.get_rect()
        attackTypeRect.update(0,0,0,0)
        #numbers
        numberImages = [pg.image.load(f"{self._finalImagePath}{num}.png") for num in range(10)]

        # Game loop   
        postHit = False         
        while runningLocal:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    runningLocal = False
                    if network:
                         self._network.send(f"deletegame {gameID}")
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        postHit = False
                        if result == ["AI", "Won"]:
                            runningLocal = False
                    elif event.key == pg.K_s:
                        self.__save() 
                        runningLocal = False
                    elif event.key == pg.K_c:
                        # Change the attacktype
                        attackType = (attackType+1)%3
                        attackTypeImage = pg.image.load(attackTypePaths[attackType])
                        attackTypeRect = attackTypeImage.get_rect()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        point = pg.mouse.get_pos()
                        if attackTypeRect.collidepoint(point): 
                            # Change the attacktype
                            attackType = (attackType+1)%3
                            attackTypeImage = pg.image.load(attackTypePaths[attackType]) 
                            attackTypeRect = attackTypeImage.get_rect()
                        for x in range(len(enemySquares)):
                            if enemySquares[x].collidepoint(point): # Checks if the mouse is inside one of the grid squares.
                                # attack that square and swap sides
                                if network:
                                    toAttack = 1
                                else:
                                    toAttack = playerNumbers[(currentPlayer+1+numAttacked) % numPlayers]

                                coords = [squareSize * round((point[0] - ((left + right//2 )% squareSize) - squareSize/2)/squareSize) + ((left + right//2) % squareSize), squareSize * round((point[1] - (top % squareSize) - squareSize/2)/squareSize) + (top % squareSize)]
                                coordinput = [(coords[0] - (left+right//2))//squareSize, (coords[1] - (top))//squareSize]

                                if attackType == 2:
                                    result = self._game.radar(toAttack)
                                    if len(result):
                                        print(result)
                                else:
                                    result = self._game.attack(coordinput[0], coordinput[1], toAttack, attackType)
                                if result == 2:
                                    numPlayers -= 1
                                    if numPlayers == 1:
                                        print(f"Player {playerNumbers[currentPlayer]+1} won!")
                                        result = [playerNumbers[currentPlayer]+1]
                                    else:
                                        print(toAttack+1, "was eliminated.")
                                        playerNumbers.remove(toAttack)
                                elif result == 1:
                                    print("Hit!")
                                    pass
                                elif result == -1:
                                    print("Miss!")
                                    pass
                                if result == -2:
                                    # error or already attacked ship
                                    print("Decrementing numAttacked.")
                                    numAttacked -= 1
                                    postHit = False

                                if network:
                                    previousAttack = self._network.send(f"updatePreviousAttack {coordinput[0]} {coordinput[1]} {playerNum} {attackType} {gameID}")
                                    x, y, attackType, pnumignore = map(int, previousAttack.split(" "))
                                    if attackType == 2:
                                        result = self._game.radar(0)
                                    else:
                                        result = self._game.attack(x, y, 0, attackType)
                                    break # Because we don't want to change the playernumber
    
                                numAttacked += 1

                                if numAttacked >= numPlayers-1:
                                    postHit = True
                                    currentPlayer = (currentPlayer + 1) % numPlayers
                                    numAttacked = 0
                                if currentPlayer == 1 and ai != 0:
                                    result = -2
                                    print("outside while")
                                    while result == -2:
                                        x,y = self._game.getAIAttack()
                                        print("inside while")
                                        result = self._game.attack(x,y,0,0)

                                    if result == 2:
                                        print("AI won!")
                                        result = [2]
                                    else:
                                        result = [x,y]

                                    currentPlayer = (currentPlayer + 1) % numPlayers
                                    numAttacked = 0

                                print(playerNumbers,currentPlayer,numAttacked)
                                break # Nothing else to do if a square has been found to be attacked.
                                
            screen.fill((0,0,0))

            if not postHit:
                myBoard = self._game.getBoard(playerNumbers[currentPlayer]) # -2,-1,0,1
                for x in range(len(squares)):
                    if myBoard[x%10][x//10] == 1:
                        pg.draw.rect(screen, (0,255,0), squares[x]) # Green fill for a ship.
                    elif myBoard[x%10][x//10] == 0:   # y coord is the % because of how I defined enemySquares.
                        pg.draw.rect(screen, (255,255,255), squares[x], 1) # White grid for an unknown
                    elif myBoard[x%10][x//10] == -1:
                        pg.draw.rect(screen, (255,0,0), squares[x]) # Red fill for a hit ship
                    else:
                        pg.draw.rect(screen, (0,0,255), squares[x]) # Blue fill for known empty
                
                enemySecretBoard = self._game.getSBoard(playerNumbers[(currentPlayer+1+numAttacked) % numPlayers])  #0 = empty, -1 = hit ship, -2 = hit empty
                for x in range(len(enemySquares)):
                    if enemySecretBoard[x%10][x//10] >= 0:   # y coord is the % because of how I defined enemySquares.
                        pg.draw.rect(screen, (255,255,255), enemySquares[x], 1) # White grid for an unknown
                    elif enemySecretBoard[x%10][x//10] == -1:
                        pg.draw.rect(screen, (255,0,0), enemySquares[x]) # Red fill for a hit ship
                    else:
                        pg.draw.rect(screen, (0,0,255), enemySquares[x]) # Blue fill for known empty

                screen.blit(attackTypeImage, attackTypeRect) # Drawin the current attack type, N, B, or R
                screen.blit(numberImages[playerNumbers[currentPlayer]+1], (0,6*self._scale)) # Drawing the current player
                screen.blit(numberImages[playerNumbers[(currentPlayer+1+numAttacked) % numPlayers]+1], (screen.get_width()-3*self._scale, screen.get_height()-5*self._scale)) # Drawing the other grid's player
            else:
                if isinstance(result, list):
                    if len(result) == 1:
                        screen.blit(numberImages[result[0]], (screen.get_width()//2, screen.get_height()//2))
                    else:
                        x,y = map(str, result)
                        count = 0
                        for ch in x:
                            ch = int(ch)
                            screen.blit(numberImages[ch], (count*self._scale*3, 0))
                            count += 1
                        
                        count += 1
                        for ch in y:
                            ch = int(ch)
                            screen.blit(numberImages[ch], (count*self._scale*3, 0))
                            count += 1
                pass
            pg.display.update()

        if network:
            self._network.send(f"deletegame {gameID}")
        elif game is not None:
            self._network.send(f"deletegame {game[1]}")

    def __addNewResolution(self, newScale):
        ogScale = 2
        scaleIncrease = newScale//ogScale
        fileNames = os.listdir("SourceImages")
        images = []
        for name in fileNames:
            images.append(Image.open(f"SourceImages\\{name}.png"))

        for x in range(len(images)):
            #resize
            n_size=(images[x].size[0]*scaleIncrease,images[x].size[1]*scaleIncrease) #output size
            res=images[x].resize(n_size,Image.Resampling.NEAREST)

            #save image
            res.save(f"FinalImages\\Scale{ogScale*scaleIncrease}\\{fileNames[x]}.png") # Scale is relative to 48 * 27 pixels

    def __help(self):
        # Initialise
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        runningHelp = True

        # Buttons
        help = pg.image.load(f"{self._finalImagePath}HelpMenu.png")

        while runningHelp:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    runningHelp = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    runningHelp = False
            screen.blit(help, (0,0))
            pg.display.update()

    def __options(self):
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        runningOptions = True
        titles = ["resolution", "length", "height", "ShipOne", "ShipTwo", "ShipThree", "ShipFour", "ShipFive", "ShipSix", "Barrage", "Radar", "Mine", "HitStreak", "numplayers"]
        changed = {}
        option = pg.image.load(f"{self._finalImagePath}OptionsMenu.png")
        result = ""

        while runningOptions:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    runningOptions = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        runningOptions = False
                    elif 48 <= event.key <= 57:
                        result += chr(event.key)
                    elif event.key == pg.K_RETURN:
                        try:
                            toChange = int(result)
                        except:
                            result = ""
                            break
                        result = ""
                        height = Game.getHeight()
                        width = Game.getWidth()
                        try:
                            newNum = int(self.__getUserInput(titles[int(toChange)-1]))
                        except Exception as e:
                            print(e, toChange)
                            break
                        print(toChange, newNum)

                        if toChange == 1:
                            self.__addNewResolution(newNum)
                            runningOptions = False
                        elif toChange == 14:
                            if newNum > 1:
                                Game.changeNumPlayers(newNum)
                            else:
                                print("Must be 2 or more players")
                            changed[int(toChange)-1] = newNum # No hints in GUI mode D: IMPORTANT PROBLEM FIX.
                        else:
                            changed[int(toChange)-2] = newNum

                        if toChange == 2:
                            Game.changeBoardDimensions(width, newNum)
                        elif toChange == 3:
                            Game.changeBoardDimensions(newNum, height)
                        elif 4 <= toChange <= 9:
                            Game.changeShips(toChange - 4, newNum)
                        elif 10 <= toChange <= 13:
                            Game.changeSpecials(toChange-10, newNum)

            screen.blit(option, (0,0))
            pg.display.update()

        with open("options.txt", "r") as f:
            data = f.readline()
            print(data)
            data = data.split(",")
        print(data)
        for index, newValue in changed.items():
            print(index)
            data[index] = str(newValue)

        with open("options.txt", "w") as f:
            f.writelines(",".join(data))

    def __load(self):
        if self._username is not None:
            loads = self._network.send(f"getLoads {self._username}")
        else:
            return

        choice = "a"
        while not choice.isnumeric():
            print("".join(loads), loads)
            choice = self.__getUserInput("".join(loads))
            if choice == "":
                return
        grids = self._network.send(f"loadGame {choice}")
        grid1, grid2, ai = grids.split(" ")
        ai = int(ai)
        Game.changeAI(ai)
        game = Game()

        for coordinate in grid1.split("|"): 
            x,y = coordinate.split(",")
            game.addShip(0, f"{x}{y}{0}{1}")

        for coordinate in grid2.split("|"):
            x,y = coordinate.split(",")
            game.addShip(1, f"{x}{y}{0}{1}")

        self.__local(False, ai, [game, False])

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

    def __authenticate(self, authtype):
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        runningAuthenticate = True
        # Buttons
        rects = []
        buttonImages = [pg.image.load(f"{self._finalImagePath}Username.png"), pg.image.load(f"{self._finalImagePath}Password.png")]
        for index, image in enumerate(buttonImages):
            rects.append(image.get_rect())
            rects[index].update(int(round((350/960)*self._width)), int(round((190/540)*self._height)) + index*int(round((110/540)*self._height)), rects[-1].width, rects[-1].height) # repostion button
        if authtype == "login":
            backGround = pg.image.load(f"{self._finalImagePath}LoginMenu.png")
        else:
            backGround = pg.image.load(f"{self._finalImagePath}SignUpMenu.png")

        password = ""
        while runningAuthenticate:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    runningAuthenticate = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    runningAuthenticate = False
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouseLocation = pg.mouse.get_pos()
                    for index, rect in enumerate(rects):
                        if rect.collidepoint(mouseLocation):
                            if index == 0:
                                self._username = self.__getUserInput("USERNAME")
                            else:
                                password = self.__getUserInput("PASSWORD")

                            if self._username != "" and password != "":
                                if authtype == "login":
                                    valid = self._network.send(f"login {self._username} {self.hash(password + self._username)}")
                                    if valid == "false":
                                        self._username =  ""
                                        password = ""
                                    else:
                                        runningAuthenticate = False
                                else:
                                    valid = self._network.send(f"signUp {self._username} {self.hash(password + self._username)}")
                                    if valid == "not_unique":
                                        self._username = ""
                                        password = ""
                                    else:
                                        runningAuthenticate = False

            for index, image in enumerate(buttonImages):
                screen.blit(image, (rects[index].left, rects[index].top))
            screen.blit(backGround, (0,0))
            pg.display.update()

        if self._username != "":
            self.__playMenu()
        else:
            return

    def __getUserInput(self, title): # returns a string
        runningUserInput = True
        re = ""
        screen = pg.display.set_mode((self._width, self._height))

        underline = pg.image.load(f"{self._finalImagePath}Underline.png")
        titleLetters = []
        for letter in title:
            titleLetters.append(pg.image.load(f"{self._finalImagePath}{letter.upper()}.png"))

        letterImages = []
        delta = 0
        while runningUserInput:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    runningUserInput = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        re = re[:-1]
                        letterImages.pop()
                    elif event.key == pg.K_LSHIFT:
                        if delta == 0:
                            delta = -32
                        else:
                            delta = 0
                    elif event.key == pg.K_ESCAPE or event.key == pg.K_RETURN:
                        runningUserInput = False
                    elif event.key == pg.K_CAPSLOCK:
                        if delta == 0:
                            delta = -32
                        else:
                            delta = 0
                    else:
                        try: 
                            chr(event.key).isalpha()
                            re += chr(event.key+delta)
                            print(event.key+delta, delta, re)
                            letterImages.append(pg.image.load(f"{self._finalImagePath}{chr(event.key).upper()}.png"))
                        except ValueError:
                            pass
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_LSHIFT:
                        if delta == 0:
                            delta = -32
                        else:
                            delta = 0

            screen.fill((0,168,243))
            position = 0
            for index, letter in enumerate(titleLetters):
                if title[index].upper() == "M" or title[index].upper() == "W":
                    letterSize = 6
                elif title[index].upper() == "Q":
                    letterSize = 5
                elif title[index].upper() == "I":
                    letterSize = 2
                elif title[index].upper() == ",":
                    letterSize = 1
                else:
                    letterSize = 4
                if title[index].isupper():
                    screen.blit(underline, (position, round(7.5*self._scale)))
                screen.blit(letter, (position, self._scale))
                position += self._scale*letterSize

            position = 0
            for index, letter in enumerate(letterImages):
                if re[index].upper() == "M" or re[index].upper() == "W":
                    letterSize = 6
                elif re[index].upper() == "Q":
                    letterSize = 5
                elif re[index].upper() == "I":
                    letterSize = 2
                else:
                    letterSize = 4
                if re[index].isupper():
                    screen.blit(underline, (position, round(self._height//2 + 6*self._scale)))
                screen.blit(letter, (position, self._height//2))
                position += self._scale*letterSize
            pg.display.update()

        print("DEBUG -- Returning re", re)
        return re

class Terminal(UI):
    def __init__(self):
        super().__init__()
        
    def run(self):
        with open("options.txt", "r") as f:
            data = f.readline()
            data = data.split(",")
        data = list(map(int, data))
        Game.changeBoardDimensions(data[0], data[1])
        for index, number in enumerate(data[2:8]):
            Game.changeShips(index, number)
        for index, number in enumerate(data[8:13]):
            Game.changeSpecials(index, number)
        Game.changeNumPlayers(data[13])
        self.__mainMenu()
    
    def __mainMenu(self):
        while True:
            print(text2art("Battleships"))
            print("Main Menu:")
            print("1. Log in")
            print("2. Sign up")
            print("3. Guest")
            print("4. Statistics")
            print("5. Quit")

            opt = input()
            if opt == "1":
                self.__logIn()
            elif opt == "2":
                self.__signUp()
            elif opt == "3":
                self.__playMenu()
            elif opt == "4":
                self.__stats()
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
            start = time.perf_counter()
            valid = self._network.send(f"login {self._username} {self.hash(password + self._username)}")
        
        print(time.perf_counter() - start)
        self.__playMenu()

    def __stats(self):
        if self._username != "":
            stats = self._network.send(f"getStats {self._username}")
        print("Format: wins,losses,hits,misses,highestHP,leastAttacks")
        input(stats)

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
        print(self._game.getSpecialCount(playerNumber)[:2]) # Don't care about mines or hitstreak
        print("0 - normal, 1 - barrage, 2 - radar")
        attackType = int(input("What attack do you want to use?"))
        if attackType <= 1:
            coordinates = input("Input square to attack (x,y), can't attack the same square twice.").split(",")
            return coordinates, attackType
        return 0, attackType

    def __local(self,aiDifficulty, game=None): # aiDifficulty is 0,1,2 or 3, 0 for no ai, and then 1,2,3 for difficulty level.
        if game is None:
            Game.changeAI(aiDifficulty)
            print("AI difficulty:", aiDifficulty)
            self._game = Game()
            numPlayers = Game.getNumPlayers()
        else:
            self._game = game[0]
            numPlayers = 2

        hints = []
        if Game.getSpecials()[4]:
            hints = [
                    ["Don't place ships to close to eachother.", "Be unpredictable", "Don't repeat what you have done previously.", "Place ships further from centre."], 
                    ["The centre is most likely to contain ships", "Attack around an already hit ship to finnish it off.", "Attack in diagonals."]
                    ]
        
        if self._username != "":
            attacks = 0
            hits = 0
            misses = 0

        if game is None:
            for playerNum in range(numPlayers): # Placing ships.
                print(f"Player {playerNum+1} turn")
                pp(self._game.getBoard(playerNum))

                numShips = Game.getNumShips()
                ships = Game.getShips()

                for ship in ships:
                    if len(hints):
                        print(random.choice(hints[0]))
                    print(f"Player {playerNum+1} to place down ship of length {ship}")
                    while self._game.addShip(playerNum, f"{self.__getShipInput(playerNum, aiDifficulty, numShips-1)}{ship}") == -1:
                        print("Invalid ship position, current state of board:")
                        pp(self._game.getBoard(playerNum))
                    numShips -= 1

                pp(self._game.getBoard(playerNum))

                input("Press enter to change turns and clear terminal")
                os.system('cls')

            print("Time to attack!")
      
        print(numPlayers)
        playerNumbers = [num for num in range(numPlayers)]
        play = True
        while play:
            choice = input("Write 's' to save, anything else to continue")
            if choice.lower() == "s":
                if numPlayers != 2:
                    print("Can only save two player games.") # IMPORANT FIX PROBLEM
                self.__save()
                break
            for playerNum in range(len(playerNumbers)):
                print(f"Player {playerNumbers[playerNum]+1} turn")
                print(f"Player {playerNumbers[playerNum]+1} board:")
                pp(self._game.getBoard(playerNumbers[playerNum]))

                if len(hints):
                    print(random.choice(hints[1]))
                for deltaPlayer in range(1, numPlayers):
                    toAttack = playerNumbers[(playerNumbers[playerNum]+deltaPlayer) % numPlayers]

                    print(f"Player {(toAttack) + 1} secret board:")
                    for row in self._game.getSBoard(toAttack): # it returns a 2d array, so we print the rows.
                        print(row)

                    result = -2
                    while result == -2: # Returing -2 = already hit square or error, -1 = miss, 1 = hit ship, 2 = game won
                        attackLocation, attackType = self.__getAttackInput(playerNumbers[playerNum], aiDifficulty)
                        result = -2
                        if attackType == 2:
                            result = self._game.radar(toAttack)
                            print(f"There is a ship at x={result[0]}, y={result[1]}")
                        else:
                            try:
                                result = self._game.attack(int(attackLocation[0]), int(attackLocation[1]), toAttack, attackType) # Index starts at 0
                            except IndexError:
                                print("Invalid attack format")

                    if result == 2:
                        numPlayers -= 1
                        if numPlayers == 1:
                            print("Hit!")
                            print(f"Player {playerNumbers[playerNum]+1} wins!")
                        else:
                            print(toAttack+1, "was eliminated.")
                            playerNumbers.remove(toAttack)
                        play = False
                    elif result == 1:
                        print("Hit!")
                    elif result == -1:
                        print("Miss!")

                    if playerNumbers[playerNum] == 0 and aiDifficulty and self._username:
                        attacks += 1
                        if result == 2:
                            hits += 1
                            self._network.send(f"updateStats {self._username} {1},{0},{hits},{misses},{self._game.getHP(0)},{attacks}")
                        elif result == 1:
                            hits += 1
                        else:
                            misses += 1
                    elif result == 2 and aiDifficulty and self._username: # AI won
                        self._network.send(f"updateStats {self._username} {0},{1},{hits},{misses},{self._game.getHP(0)},{attacks}")

                input("Press enter to change turns and clear terminal")
                os.system('cls')

        if game is not None:
            self._network.send(f"deletegame {game[1]}")

    def __networkGame(self):
        self._game = Game()
        if self._username == "":
            print("Must be logged in!")
            return
        print(text2art("Online"))
        enemyName = input("What is your enemy's username?")
        print("Setting up game with opponent...")
        playerNum, gameID = self._network.send(f"startGame {self._username} {enemyName}").split(" ")
        playerNum = int(playerNum[1]) - 1

        # get and compare player statistics
        hits = 0
        misses = 0

        myStats = self._network.send(f"getStats {self._username}") # wins,losses,hits,misses,highestHP,leastAttacks
        enemyStats = self._network.send(f"getStats {enemyName}")
        print(myStats, enemyStats)
        if myStats != "None" and enemyStats != "None":
            needsHelp = self.compareStats(myStats, enemyStats)
        else:
            needsHelp = -1
        if needsHelp != -1:
            print(f"It is recommended that player {needsHelp+1} gets help.")
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
                hits += 1
                print("Hit!")
                print(f"Player {playerNum+1} wins!")
                play = False
                self._network.send(f"updateStats {1},{0},{hits},{misses},{0},{10000000}")
            elif result == 1:
                hits += 1
                print("Hit!")
            elif result == -1:
                misses += 1
                print("Miss!")
            
            previousAttack = self._network.send(f"updatePreviousAttack {attackLocation[0]} {attackLocation[1]} {playerNum} {attackType} {gameID}")
            print("Enemy player attacked - ", previousAttack)
            x, y, attackType, pnumignore = map(int, previousAttack.split(" "))
            result = self._game.attack(x, y, playerNum, attackType)
            if result == 2:
                self._network.send(f"updateStats {0},{1},{hits},{misses},{0},{10000000}")
                play = False

        self._network.send(f"deletegame, {gameID}")

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
            print(f"13. Hints {specialsCounts[4]}")
            print(f"14. Number of players {numPlayers}")
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
            elif 9 <= int(toChange) <= 13:
                Game.changeSpecials(int(toChange)-9, newNum)
            elif toChange == "14":
                if newNum > 1:
                    Game.changeNumPlayers(newNum)
                else:
                    print("Must be 2 or more players")

        with open("options.txt", "r") as f:
            data = f.readline().split(",")
        print(data)
        for index, newValue in changed.items():
            data[index] = str(newValue)

        with open("options.txt", "w") as f:
            f.writelines(data)

    def __load(self):
        if self._username is not None:
            loads = self._network.send(f"getLoads {self._username}")
        for load in loads.split(","):
            print(load)

        choice = input("Which game would you like to load?")
        if choice.upper() == "E":
            return
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

        self.__local(ai, [game, int(choice)])

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