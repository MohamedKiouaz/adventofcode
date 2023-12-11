import numpy as np
from itertools import combinations
import scipy.sparse as sps

with open('2023/11/11.txt') as f:
    content = f.readlines()


n_content = [[-1 if k == '#' else 0 for k in x.strip()] for x in content]
array = sps.csr_array(n_content)

print(array.shape)

N = 1_000_000 - 1

# duplicate the lines where sum == 0
i = np.longlong(0)
while i < array.shape[0]:
    if array[[i], :].sum() == 0:
        zero_row = sps.csr_matrix((N, array.shape[1]))
        array = sps.vstack([array[:i, :], zero_row, array[i:, :]])
        i = i + N
    i = i + 1

# same with columns
i = 0
while i < array.shape[1]:
    if array[:, i].sum() == 0:
        zero_col = sps.csr_matrix((array.shape[0], N))
        array = sps.hstack([array[:, :i], zero_col, array[:, i:]])
        i = i + N
    i = i + 1

print(array.shape)

galaxies_x, galaxies_y = array.nonzero()
galaxies = list(zip(galaxies_x, galaxies_y))

print(len(list(combinations(galaxies, 2))))

total = np.longlong(0)
for p1, p2 in combinations(galaxies, 2):
    total += np.abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

print(total)