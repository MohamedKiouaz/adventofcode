import numpy as np

with open('2023/10/10s4.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]

connections = {'|': ['N', 'S'], '-': ['E', 'W'], 'L': ['N', 'E'], 'J': ['N', 'W'], '7': ['S', 'W'], 'F': ['S', 'E']}

cardinals = {'N': np.array([-1, 0]), 'S': np.array([1, 0]), 'E': np.array([0, 1]), 'W': np.array([0, -1])}

grid = np.ones((len(content), len(content[0])), dtype=np.int32) * -1

for i_, line in enumerate(content):
    for j_, char in enumerate(line):
        if char == 'S':
            grid[i_, j_] = 0
            break

step = 0
while True:
    # find coordinates of the current position
    current_positions = np.where(grid == step)

    if len(current_positions[0]) == 0:
        break

    for i_, j_ in zip(current_positions[0], current_positions[1]):
        for i, j in [[0, -1], [0, 1], [1, 0], [-1, 0]]:
            ii = i_ + i
            jj = j_ + j
            if ii < 0 or ii >= len(content) or jj < 0 or jj >= len(content[0]):
                continue

            if grid[ii, jj] != -1:
                continue

            if content[ii][jj] in connections:
                # check if the connection is valid
                cards = connections[content[ii][jj]]

                for card in cards:
                    card_pos = cardinals[card]

                    if ii + card_pos[0] < 0 or ii + card_pos[0] >= len(content) or jj + card_pos[1] < 0 or jj + card_pos[1] >= len(content[0]):
                        continue
                    
                    if grid[ii + card_pos[0], jj + card_pos[1]] == step:
                        grid[ii, jj] = step + 1
    
    step += 1

connex = np.ones_like(grid) * -1

def grow(i, j, grid, connex):
    for ii in range(i - 1, i + 2):
        for jj in range(j - 1, j + 2):
            if ii < 0 or ii >= connex.shape[0] or jj < 0 or jj >= connex.shape[1]:
                continue

            if grid[ii, jj] != -1 or connex[ii, jj] != -1:
                continue

            connex[ii, jj] = connex[i, j]

            connex = grow(ii, jj, grid, connex)

    return connex

for i in [0, connex.shape[0] - 1]:
    for j in range(connex.shape[1]):
        if grid[i, j] != -1:
            continue

        connex[i, j] = 0
        
        connex = grow(i, j, grid, connex)   

for j in [0, connex.shape[1] - 1]:
    for i in range(connex.shape[0]):
        if grid[i, j] != -1:
            continue

        connex[i, j] = 0
        
        connex = grow(i, j, grid, connex)

print(grid)

for i in range(connex.shape[0]):
    for j in range(connex.shape[1]):
        if grid[i, j] != -1 or connex[i, j] != -1:
            continue
        
        connex[i, j] = connex.max() + 1

        connex = grow(i, j, grid, connex)

for line in connex:
    print(''.join([str(x)[-1] if x != -1 else '.' for x in line])) 

print(connex.max())