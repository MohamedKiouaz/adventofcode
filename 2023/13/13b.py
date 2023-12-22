import numpy as np
from tqdm import tqdm
from itertools import combinations

def to_num(line):
    return [int(x == '#') for x in line]

with open('2023/13/13.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]
content = [to_num(x) for x in content]

tables = []

s = 0
for i, c in enumerate(content):
    if c == []:
        tables += [np.array(content[s:i])]
        s = i + 1

tables += [np.array(content[s:])]

print(f"Found {len(tables)} tables.")
print("Last table:")
print(tables[-1])

total = 0

for n_table, table in enumerate(tables):
    print(f"Table {n_table}:")
    
    for i in range(table.shape[0] - 1):
        # print(f"Checking line {i}")
        ok = 0
        for j in range(table.shape[0]):
            # print(f"Checking lines {i - j} and {i + 1 + j}")
            if i - j < 0 or i + 1 + j >= table.shape[0]:
                break

            # print(table[i - j])
            # print(table[i + 1 + j])

            ok += (table[i - j] != table[i + 1 + j]).sum()

            if ok > 1:
                break
        print(f"ok = {ok}")
        if ok == 1:
            print(f"reflexion found between lines {i} and {i + 1}")

            total += 100 * (i +1)

    for i in range(table.shape[1] - 1):
        # print(f"Checking line {i}")
        ok = 0
        for j in range(table.shape[1]):
            # print(f"Checking lines {i - j} and {i + 1 + j}")
            if i - j < 0 or i + 1 + j >= table.shape[1]:
                break

            # print(table[i - j])
            # print(table[i + 1 + j])

            ok += (table[:, i - j] != table[:, i + 1 + j]).sum()
            # print(f"reflexion not found between lines {i} and {i + 1}")
            if ok > 1:
                break
            
        if ok == 1:
            print(f"reflexion found between columns {i} and {i + 1}")

            total += i + 1

print(total)
        
