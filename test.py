import numpy as np

arr = np.array([1,3,4,5])
b = np.array([i for i in arr if i >= 4 or i <= 2])
print(b)