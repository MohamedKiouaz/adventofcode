import numpy as np
from itertools import combinations

with open('2023/11/11.txt') as f:
    content = f.readlines()


n_content = [[-1 if k == '#' else 0 for k in x.strip()] for x in content]
array = np.array(n_content)

print(array.shape)

# duplicate the lines where sum == 0
i = 0
while i < array.shape[0]:
    if array[i, :].sum() == 0:
        array = np.insert(array, i, array[i, :], axis=0)
        i = i + 1
    i = i + 1
# same with columns
i = 0
while i < array.shape[1]:
    if array[:, i].sum() == 0:
        array = np.insert(array, i, array[:, i], axis=1)
        i = i + 1
    i = i + 1

def show(array):
    for line in array:
        print(''.join(['#' if x == -1 else '.' for x in line]))

print(array.shape)

galaxies_x, galaxies_y = np.where(array == -1)
galaxies = list(zip(galaxies_x, galaxies_y))

total = 0
for p1, p2 in combinations(galaxies, 2):
    total += abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

print(total)