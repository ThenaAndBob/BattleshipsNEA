from abc import abstractclassmethod
from Game import Game


class UI():
    def __init__(self):
        pass

    @abstractclassmethod
    def run():
        raise NotImplementedError

class GUI(UI):
    def __init__(self):
        super().__init__()

    def run(self):
        self._game = Game()

class Terminal(UI):
    def __init__(self):
        super().__init__()

    def run(self):
        self._game = Game()

