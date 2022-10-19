from abc import abstractclassmethod
import math
from Game import Game
from pprint import pprint as pp
import os
import pygame as pg
from art import *

class UI():
    def __init__(self):
        self._game = Game()
        self._numTurns = 4

    @abstractclassmethod
    def run():
        raise NotImplementedError

class GUI(UI):
    def __init__(self):
        super().__init__()

    def run(self):
        self.__menu()

    def __menu(self):
        # Initialise
        pg.init()
        WIDTH = 400
        HEIGHT = 400
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        running = True

        # Buttons
        rects = []
        buttonImages = [pg.image.load("play.png"), pg.image.load("help.png"), pg.image.load("quit.png")] # .convert() ?
        for x in buttonImages:
            rects.append(x.get_rect())
        #reposition these rects correctly.

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Check which menu button it collided with and call that function.
                        point = pg.mouse.get_pos
                        for x in range(len(rects)):
                            if rects[x].collidepoint(point):
                                if x == 0:
                                    self.__playMenu()
                                elif x == 1:
                                    self.__help()
                                else:
                                    running = False
                                    pg.quit()

    def __playMenu():
        pass

    def __local(self):
        # Initialise
        pg.init()
        WIDTH = 600
        HEIGHT = 400
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        running = True
        currPlayer = 0

        # Ships
        rects = []
        shipAttach = [False, False, False]
        shipImages = [pg.image.load("ship1"), pg.image.load("ship2"), pg.image.load("ship3")] # .convert() ?
        for x in shipImages:
            rects.append(x.get_rect())
            #scale these correctly, each square is 40*40 pixels.

        # Grid
        squareSize = 40
        squares = []
        for x in range(200, WIDTH, squareSize):
            for y in range(0, HEIGHT, squareSize):
                squares.append(pg.Rect(x, y, squareSize, squareSize))

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1 and True not in shipAttach:
                        point = pg.mouse.get_pos()
                        for x in range(len(rects)):
                            if rects[x].collidepoint(point):
                                # Mouse attaches to ship and starts moving it around.
                                shipAttach[x] = True
                                pass
                elif event.type == pg.MOUSEBUTTONDOWN and True in shipAttach:
                    point = pg.mouse.get_pos()
                    # if this ship can be placed do:
                    for x in range(len(shipAttach)):
                        if shipAttach[x]:
                            shipAttach[x] = False
                            rects[x].left = 20 * math.round((point[0] - rects[x].width/2)/20)   # rounded to nearest 20
                            rects[x].top = 20 * math.round((point[1] - rects[x].height/2)/20)
                            self._game.addShip(currPlayer, f"{(rects[x].left - 200)/20}{(rects[x].top - 200)/20}h3")
                            break

            for x in range(len(shipAttach)): # Makes a ship follow the mouse around once it has been clicked.
                if shipAttach[x]:
                    rects[x].left = pg.mouse.get_pos()[0] + rects[x].width/2
                    rects[x].top = pg.mouse.get_pos()[1] + rects[x].height/2

            for square in squares:
                pg.draw.rect(screen, (255,255,255), square, 1)

            for x in range (len(rects)):
                screen.blit(shipImages[x], rects[x])

    def __help():
        pass

    def __placeShips(self):
        pass

    def __displayBoard(self):
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
            y = self._numTurns
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
                for x in self._game.getSBoard(x):
                    print(x)

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

    
