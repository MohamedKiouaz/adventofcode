import numpy as np
import sys
import tqdm

sys.setrecursionlimit(2000000000)

with open('2023/10/10.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]

# unicode replacement for edges
content_rewritten = [x.replace('L', '└').replace('J', '┘').replace('7', '┐').replace('F', '┌').replace('|', '│').replace('-', '─') for x in content]

for line in content_rewritten:
    print(line)

connections = {'|': ['N', 'S'], '-': ['E', 'W'], 'L': ['N', 'E'], 'J': ['N', 'W'], '7': ['S', 'W'], 'F': ['S', 'E']}

cardinals = {'N': [-1, 0], 'S': [1, 0], 'E': [0, 1], 'W': [0, -1]}

grid = np.ones((len(content), len(content[0])), dtype=np.int32) * -1

for i_, line in enumerate(content):
    for j_, char in enumerate(line):
        if char == 'S':
            grid[i_, j_] = 0
            break

print(grid.size)

step = 0
while True:
    # find coordinates of the current position
    current_positions = np.where(grid == step)

    if len(current_positions[0]) == 0:
        print(f'no more positions at step {step}')
        break

    for i_, j_ in zip(current_positions[0], current_positions[1]):
        cards_to_explore = connections[content[i_][j_]] if content[i_][j_] != 'S' else ['N', 'E', 'W', 'S']
        for card_ in cards_to_explore:
            i, j = cardinals[card_]
            ii = i_ + i
            jj = j_ + j
            if ii < 0 or ii >= len(content) or jj < 0 or jj >= len(content[0]):
                continue

            if grid[ii, jj] != -1:
                continue

            if content[ii][jj] not in connections:
                continue
            
            # check if the connection is valid
            for card in connections[content[ii][jj]]:
                card_x, card_y = cardinals[card]

                if ii + card_x < 0 or ii + card_x >= len(content) or jj + card_y < 0 or jj + card_y >= len(content[0]):
                    continue
                
                if grid[ii + card_x, jj + card_y] == step:
                    grid[ii, jj] = step + 1
        
    step += 1

print(f"max step: {grid.max()}")

print(grid)

def explore(m, i, j):
    if m[i, j] == m.max():
        return [(i, j)]
    stack = [(i, j, [(i, j)])]  # Initialize stack with starting coordinates and path
    visited = set()
    while stack:
        i, j, path = stack.pop()

        if (i, j) in visited:
            continue
        
        visited.add((i, j))
        
        for ii in range(i - 1, i + 2):
            for jj in range(j - 1, j + 2):
                # Check boundary conditions
                if ii < 0 or ii >= m.shape[0] or jj < 0 or jj >= m.shape[1]:
                    continue
                # Check value increment condition
                if m[ii, jj] != m[i, j] + 1:
                    continue

                # Check if the maximum value is reached
                if m[ii, jj] == m.max():
                    return path + [(ii, jj)]

                # Add the next coordinates and updated path to the stack
                stack.append((ii, jj, path + [(ii, jj)]))

    return []

print(grid)
print("adada")
loop = []
xx, yy = np.where(grid == 1)
for x, y in zip(xx, yy):
    print(f'exploring {x}, {y}')
    g = grid.copy()
    for i, j in loop:
        g[i, j] = 0
    print(g)
    loop.extend(explore(g, x, y))
    print(len(loop))

mask = np.zeros_like(grid)
for x, y in loop:
    mask[x, y] = 1

print('mask')
print(mask)

for i, line in enumerate(content_rewritten):
    for j, char in enumerate(line):
        if mask[i][j] == 1:
            print(char, end='')
        elif char == '.':
            print('.', end='')
        else:
            print(' ', end='')
    print()

print("done mask")

grid[1 - mask] = -1

# connex = np.ones_like(grid) * -1

# def grow(i, j, grid, connex):
#     for ii in range(i - 1, i + 2):
#         for jj in range(j - 1, j + 2):
#             if ii < 0 or ii >= connex.shape[0] or jj < 0 or jj >= connex.shape[1]:
#                 continue

#             if grid[ii, jj] != -1 or connex[ii, jj] != -1:
#                 continue

#             connex[ii, jj] = connex[i, j]

#             connex = grow(ii, jj, grid, connex)

#     return connex

# for i in [0, connex.shape[0] - 1]:
#     for j in range(connex.shape[1]):
#         if grid[i, j] != -1:
#             continue

#         connex[i, j] = 0
        
#         connex = grow(i, j, grid, connex)   

# for j in [0, connex.shape[1] - 1]:
#     for i in range(connex.shape[0]):
#         if grid[i, j] != -1:
#             continue

#         connex[i, j] = 0
        
#         connex = grow(i, j, grid, connex)

# print(grid)

# for i in range(connex.shape[0]):
#     for j in range(connex.shape[1]):
#         if grid[i, j] != -1 or connex[i, j] != -1:
#             continue
        
#         connex[i, j] = connex.max() + 1

#         connex = grow(i, j, grid, connex)

# for line in connex:
#     print(''.join([str(x)[-1] if x != -1 else '.' for x in line])) 

relevant_edges = {'|', 'L', 'J', '7', 'F', 'S'}

inside = np.zeros_like(grid)

crossed = np.zeros_like(grid)

print(grid.shape)

for i in range(grid.shape[0]):
    crossed_edges = 0
    last = ''
    for j in range(grid.shape[1]):
        c = content[i][j]
        c = c.replace('S', 'L')
        if c in relevant_edges and grid[i, j] != -1:
            if last == 'L' and c == '7' or last == 'F' and c == 'J' or last == 'J' and c == 'F' or last == '7' and c == 'L':
                crossed_edges += 1
                last = ''
            if c == 'L' or c == 'F' or c == '7' or c  == 'J':
                last = c
            if c == '|':
                crossed_edges += 1
            # crossed_edges += 1
        elif crossed_edges % 2 == 1 and grid[i, j] == -1:
            inside[i, j] = 1
        
        crossed[i][j] = crossed_edges%2

for line in crossed:
    print(''.join([str(x) if x != -1 else '.' for x in line]))

for line in inside:
    print(''.join([str(x) if x == 1 else '.' for x in line]))

print(inside.sum())