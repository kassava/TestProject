import math

# value1 = math.pow(math.pow(5, 2), math.pow(5, 3)) * math.pow(50, 100) * math.pow(25, -137)
# value2 = math.pow(100, 50) * math.pow(math.pow(5, 3), math.pow(5, 2))
# value = value1 / value2
import numpy as np

a = np.eye(3, 4, k = 0)
b = np.eye(3, 4, k = 1)
a = a * 2 + b
print(np.eye(3, 4, k = 0) * 2 + np.eye(3, 4, k = 1))