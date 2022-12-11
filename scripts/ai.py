import numpy as np
from pprint import pprint
import time

class AI():
    def __init__(self):
        self.SHIP_SIZES = [2,3,4,5]
        self.SHOT_MAP = np.zeros([10, 10])

    def gen_prob_map(self):
        prob_map = np.zeros([10, 10])
        for ship_size in self.SHIP_SIZES:
            use_size = ship_size - 1
            # check where a ship will fit on the board
            for row in range(10):
                for col in range(10):
                    if self.SHOT_MAP[row][col] != 1:
                        # get potential ship endpoints
                        endpoints = []
                        # add 1 to all endpoints to compensate for python indexing
                        if row - use_size >= 0:
                            endpoints.append(((row - use_size, col), (row + 1, col + 1)))
                        if row + use_size <= 9:
                            endpoints.append(((row, col), (row + use_size + 1, col + 1)))
                        if col - use_size >= 0:
                            endpoints.append(((row, col - use_size), (row + 1, col + 1)))
                        if col + use_size <= 9:
                            endpoints.append(((row, col), (row + 1, col + use_size + 1)))
                        pprint(endpoints)
                        for (start_row, start_col), (end_row, end_col) in endpoints:
                            if np.all(self.SHOT_MAP[start_row:end_row, start_col:end_col] == 0):
                                prob_map[start_row:end_row, start_col:end_col] += 1
        return prob_map

timeS = time.perf_counter()
myAI = AI()
pprint(myAI.gen_prob_map())
print(time.perf_counter() - timeS)