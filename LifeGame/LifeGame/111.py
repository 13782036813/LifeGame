import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

a = np.array([[1,2,3],
            [4,5,6],
            [7,8,9]])

a_padded = np.pad(a, pad_width=1 , mode='constant')
print(a_padded)
top = a_padded[:-2, 1:-1]  # 上
print("top:")
print(top)
bottom = a_padded[2:,1:-1]
print("bottom:")
print(bottom)
