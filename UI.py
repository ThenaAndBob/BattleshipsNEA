from abc import abstractclassmethod
from Game import Game
from pprint import pprint as pp
import os

class UI():
    def __init__(self):
        self._game = Game()

    @abstractclassmethod
    def run():
        raise NotImplementedError

class GUI(UI):
    def __init__(self):
        super().__init__()

    def run(self):
        pass

class Terminal(UI):
    def __init__(self):
        super().__init__()
        self._numTurns = 4

    def run(self):
        for x in range(2):
            print(f"Player {x+1} turn")
            pp(self._game.getBoard(x))
            y = self._numTurns
            while y > 0:
                if self._game.addShip(x, input((f"{y} Ships in format xyrh"))) == -1:
                    print("Ships overlap, current state of board:")
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
                    attack = input("Input square to attack (xy)")
                    result = self._game.Attack(int(attack[0]), int(attack[1]), (x+1)%2)
                    if result == 3:
                        print("Hit!")
                        print(f"Player {x+1} wins!")
                        play = False
                        break
                    elif result == 1:
                        print("Hit!")
                    elif result == -1 or result == 2:
                        print("Miss!")
                    input("Press enter to change turns and clear terminal")
                os.system('cls||clear')


