from abc import abstractclassmethod
from Game import Game
from pprint import pprint as pp
import os
import pygame as pg
from art import *
from network import Network

class UI():
    def __init__(self):
        self._game = Game()
        try:
            #self._network = Network()
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
    def __signUp():
        raise NotImplementedError

    @abstractclassmethod
    def __logIn():
        raise NotImplementedError

    @abstractclassmethod
    def __help():
        raise NotImplementedError

    def hash(self, password):
        return password

class GUI(UI):
    def __init__(self):
        super().__init__()
        self._scale = 20
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
        buttonImages = [pg.image.load(f"FinalImages\Scale{self._scale}\LoginButton.png"), pg.image.load(f"FinalImages\Scale{self._scale}\SignUpButton.png"), pg.image.load(f"FinalImages\Scale{self._scale}\GuestButton.png"), pg.image.load(f"FinalImages\Scale{self._scale}\QuitButton.png")] 
        backgroundImage = pg.image.load(f"FinalImages\Scale{self._scale}\MainMenu.png") 
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
                                    self.__local()
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
        buttonImages = [pg.image.load(f"FinImages\Play{self._scale}.png"), pg.image.load(f"FinImages\Help{self._scale}.png"), pg.image.load(f"FinImages\Quit{self._scale}.png")] 
        backgroundImage = pg.image.load(f"FinImages\MenuBackGround{self._scale}.png") 
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
                                    self.__local()
                                elif i == 1:
                                    self.__help()
                                else:
                                    running = False
                                    pg.quit()

            screen.blit(backgroundImage, (0,0))
            for x in range (len(rects)):
                screen.blit(buttonImages[x], rects[x])

            pg.display.update()

    def __local(self):
        # Initialise
        pg.init()
        screen = pg.display.set_mode((self._width, self._height))
        running = True
        currentPlayer = 0

        # Ships
        rects = []
        shipAttach = [0, 0, 0]
        shipImages = [pg.image.load(f"FinalImages\Scale{self._scale}\HP2Ship.png"), pg.image.load(f"FinalImages\Scale{self._scale}\HP2Ship.png"), pg.image.load(f"FinalImages\Scale{self._scale}\HP2Ship.png")] 
        shipHP = [2, 2, 2, 2]
        shipRotation = [0, 0, 0]
        shipLoc = [[[0, 0] for _ in range(len(shipAttach))], [[0,0] for _ in range(len(shipAttach))]] # Stores the top and left coordinates of ships.
        for x in range(len(shipImages)):
            rects.append(shipImages[x].get_rect())
            #scale these correctly, each square is 40*40 pixels.

        # Buttons
        buttonImages = [pg.image.load(f"FinalImages\Scale{self._scale}\HP2Ship.png")]
        buttonRects = []
        for x in range(len(buttonImages)):
            buttonRects.append(buttonImages[x].get_rect())
        buttonRects[0].update(0, self._height-(2*buttonRects[0].height), buttonRects[0].width, buttonRects[0].height)

        # Grid
        WidthInSquares = 10 # Dimensions of the grid in squares.
        HeightInSquares = 10 
        squareSize = self._height//(HeightInSquares+1) # +1 to give a little bit of space.
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
                                self._game.addShip(currentPlayer, f"{(rects[x].left - left)//squareSize}{(rects[x].top-top)//squareSize}{shipRotation[x]}{shipHP[x]}")
                                shipLoc[currentPlayer][x] = [rects[x].left, rects[x].top]
                                rects[x].update(0, 0, rects[x].width, rects[x].height) # Should probably also rotate these back to horizontal to not spoil
                            if currentPlayer == 0:
                                currentPlayer = 1
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
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        point = pg.mouse.get_pos()
                        for x in range(len(enemySquares)):
                            if enemySquares[x].collidepoint(point): # Checks if the mouse is inside one of the grid squares.
                                # attack that square and swap sides
                                coords = [squareSize * round((point[0] - ((left + right//2 )% squareSize) - squareSize/2)/squareSize) + ((left + right//2) % squareSize), squareSize * round((point[1] - (top % squareSize) - squareSize/2)/squareSize) + (top % squareSize)]
                                coordinput = [(coords[0] - (left+right//2))//squareSize, (coords[1] - (top))//squareSize]
                                result = self._game.attack(coordinput[0], coordinput[1], (currentPlayer+1) % 2)
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
            username = input("Username - ")
            password = input("Password - ")
            if " " in username or " " in password:
                print("Username or password cannot have spaces!")
            else:
                valid = self._network.send(f"signUp {username} {self.hash(password)}")
            print("")
            
        self.__playMenu()

    def __logIn(self):
        valid = "false"
        while valid == "false":
            username = input("Username - ")
            password = input("Password - ")
            print("")
            valid = self._network.send(f"login {username} {self.hash(password)}")
        
        self.__playMenu()

    def __playMenu(self):
        while True:
            print(text2art("Battleships"))
            print("1. Local")
            print("2. Network")
            print("3. AI Opponent")
            print("4. Help")
            print("5. Options")
            print("6. Quit")
            opt = input()
            if opt == "1":
                self.__local(0) # No ai
            elif opt == "2":
                self.__network()
            elif opt == "3":
                self.__local(input("What AI difficulty? 1,2 or 3"))
            elif opt == "4":
                self.__help()
            elif opt == "5":
                self.__options()
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
            return input("Input square to attack (xy), can't attack the same square twice."), attackType
        return 0, attackType

    def __local(self,aiDifficulty): # aiDifficulty is 0,1,2 or 3, 0 for no ai, and then 1,2,3 for difficulty level.
        Game.changeAI(aiDifficulty)
        print("AI difficulty:", aiDifficulty)
        self._game = Game()
        numPlayers = Game.getNumPlayers()

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
                    numShips += 1
                numShips -= 1

            pp(self._game.getBoard(playerNum))

            input("Press enter to change turns and clear terminal")
            os.system('cls')

        print("Time to attack!")
        play = True
        while play:
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

    def __network(self):
        pass

    def __help(self):
        print("Advice")

    def __options(self):
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
                return

            newNum = inp.split(" ")[1]
            if newNum.isnumeric():
                newNum = int(newNum)
            else:
                newNum = bool(newNum)

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
                    print("Must be more than 2 or more players")




