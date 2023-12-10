from bisect import bisect_left
from functools import reduce
import math
import numpy as np
from tqdm import tqdm

def ppcm(a, b):
    return abs(a*b) // math.gcd(a, b)

with open('2023/8/8.txt') as f:
    content = f.readlines()

path = content[0].strip()

def work(line):
    line = line.replace('(', '').replace(')', '')
    origin, destinations = line.split('=')
    destinations = [k.strip() for k in destinations.split(',')]

    return origin.strip(), destinations

content = list(map(work, content[2:]))
map_ = {origin:destinations for origin, destinations in content}

print(map_)

m = {}
for origin, destinations in map_.items():
    for i, e in enumerate(path):
        index = int(e == "R")
        m[str(i)+origin] = str((i + 1) % len(path)) + destinations[index]

print(m)

currents = ['0' + k for k in map_.keys() if k.endswith('A')]

print(len(currents))

def test(L):
    state = [[0, 0] for k in range(len(L))]
    for i, l in enumerate(L):
        nodes = [k for k, _ in l]
        unique_nodes = set(nodes)
        
        for node in unique_nodes:
            if nodes.count(node) != 2:
                continue
            
            for n_, v in l:
                if n_ == node:
                    state[i][0] = v
                    break
            for n_, v in l[::-1]:
                if n_ == node:
                    state[i][1] = v
                    break

        if state[i][0] == 0 or state[i][1] == 0:
            print(f"no answer for {i}")
            return

    print(state)

    # N = np.zeros((len(state), len(state)))
    # R = np.zeros((len(state), 1))
    # for i in range(len(state) - 1):
    #     offset, length = state[i]
    #     offset_next, length_next = state[i + 1]
    #     N[i, i] = length - offset
    #     N[i, i + 1] = -(length_next + offset_next)
    #     R[i, 0] = offset_next - offset

    # res = np.linalg.solve(N, R).astype(int)
    # if any(res < 0):
    #     print("negative solution", res)

    # for i, n in enumerate(res):
    #     offset, length = state[i]
    #     print(f"{offset + n * (length - offset)}")

    sums = np.array([0 for k in range(len(state))]).astype(np.ulonglong)
    total = 2_000_000_000_000
    with tqdm(total=total) as pbar:
        while max(sums) < total:
            arg_min = np.argmin(sums)
            offset, length = state[arg_min]
            sums[arg_min] += length - offset

            if all([sums[i] == sums[i + 1] for i in range(len(sums) - 1)]):
                print("maybe answer", sums[0])
            
            pbar.update(max(sums) - pbar.n)

    # candidates = []
    # for offset, length in state:
    #     n = 0
    #     i = 0
    #     while n < 2_000_000_000_000:
    #         n = offset + i * (length - offset)
    #         i += 1
    #         candidates.append(n)
    #         if i % 100_000 == 0:
    #             print(i, n)

    # unique_candidates = set()
    # for k in candidates:
    #     unique_candidates.update(k)

    # for k in unique_candidates:
    #     closest = [bisect_left(c, k) for c in candidates]
    #     if not all([closest[i] < len(candidates) for i in range(len(candidates))]):
    #         continue

    #     if all([k == c for c in closest]):
    #         print("maybe answer", k)
    
    print("That's all folks")

times = [[] for k in  range(len(currents))]
len_times = 0
i = 0
while any([not current.endswith('Z') for current in currents]):
    currents = [m[current] for current in currents]

    for j, current in enumerate(currents):
        already_reached = [k for k, _ in times[j]]
        if current.endswith('Z') and already_reached.count(current) < 2:
            times[j].append((current, i))

    new_len_times = sum([len(k) for k in times])
    if new_len_times != len_times:
        len_times = new_len_times
        print(times)
        test(times)
    
    i += 1
    if i % 1_000_000 == 0:
        print(i)

    # if all([len(k) > 0 for k in  times]):
    #     t_ = [k[1] for k in times]
    #     if n != reduce(ppcm, t_):
    #         n = reduce(ppcm, t_)

print(times)