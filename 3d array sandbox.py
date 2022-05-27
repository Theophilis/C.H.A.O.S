import numpy as np


fives = np.zeros((5, 5, 5), dtype='int8')
count = 0
for x in range(5):

    for y in range(5):

        for z in range(5):

            fives[x, y, z] = count

            count += 1

print(fives)