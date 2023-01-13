import time
from math import sqrt

start = time.perf_counter()
a = 194894218491 ** 0.5
time1 = time.perf_counter() - start

start = time.perf_counter()
b = sqrt(194894218491)
time2 = time.perf_counter() - start

print(time1, time2, time1-time2)
print(a,b)
