from abc import abstractclassmethod
from Game import Game
from pprint import pprint as pp
import os
import pygame

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
        self._numTurns = 4

    def run(self):
        self._menu()
        pass

    def _menu(self):
        pygame.init()

        menuOptLoc = []
        pointerLoc = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT():
                    running = False

        pygame.QUIT

class Terminal(UI):
    def __init__(self):
        super().__init__()

    def run(self):
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


