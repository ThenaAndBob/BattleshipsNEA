from abc import abstractclassmethod
from Game import Game
from pprint import pprint as pp

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

    def run(self):
        for x in range(2):
            print(f"Player {x+1} turn")
            pp(self._game.getBoard(x))
            for y in range(4, 0 , -1):
                self._game.addShip(x, input((f"{y} Ships in format xyrh")))
            pp(self._game.getBoard(x))

        print("Time to attack!")
        play = True
        while play:
            for x in range(2):
                print("\n\n\n")
                print(f"Player {x+1} turn")
                attack = input("Input square to attack (xy)")

                result = self._game.Attack(int(attack[0]), int(attack[1]), (x+1)%2)
                if result == 2:
                    print("Hit!")
                    print(f"Player {x+1} wins!")
                    play = False
                    break
                elif result == 1:
                    print("Hit!")
                else:
                    print("Miss!")


