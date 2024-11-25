

import numpy as np

arr = np.array([
    [1,2,3],
    [2,3,4]
])

ser = arr.tobytes()

print(arr.shape)
print(ser)

des = np.frombuffer(ser, dtype=np.float32).reshape((1, 15, 3))
print(des)
