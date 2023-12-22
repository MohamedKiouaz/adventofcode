import numpy as np
from tqdm import tqdm
from itertools import combinations

def split(line):
    s, goal = line.split(' ')
    goal = tuple(int(g) for g in goal.split(','))

    return s, goal

calls = 0

def work(splitted_line, idx=0):
    global calls
    calls += 1

    s, goal = splitted_line
    sgoal = sorted(goal, reverse=True)

    diese_count = s.count('#')
    question_count = s.count('?')

    if idx >= len(goal) or diese_count == sum(goal):
        s = s.replace('?', '.')
    if diese_count + question_count == sum(goal) :
        s = s.replace('?', '#')
    
    blocks = [x for x in s.split('.')]

    # print(s, goal, idx)

    clean_blocks = [x for x in blocks if x != '']

    i = 0
    while i < len(clean_blocks):
        if i >= len(clean_blocks) or i >= len(goal) or '?' in clean_blocks[i]:
            break
        if len(clean_blocks[i]) != goal[i]:
            return []
        i += 1
    
    if idx == 0:
        clean_blocks_len = [len(x) for x in clean_blocks if '?' not in x]
        clean_blocks_len = sorted(clean_blocks_len, reverse=True)

        i = 0
        while i < len(clean_blocks_len) and clean_blocks_len[i] == sgoal[i]:
            i += 1

        if i > 0:
            return work((s, goal), i)

    if not '?' in s and len(clean_blocks) == len(goal):
        if all([len(x) == goal[i] for i, x in enumerate(clean_blocks)]):
            return [s]
        return []
    
    if idx == len(goal):
        return []
    
    search_number = sgoal[idx]

    ret = []
    once = False
    for block_number, block in enumerate(blocks):
        if len(block) < search_number:
            continue
        
        if '?' not in block and not once:
            ret += work((s, goal), idx+1)
            once = True

        for i in range(len(block) - search_number + 1):
            new_block = block[:i] + '#' * search_number + block[i+search_number:]
            new_block = list(new_block)

            if i > 0:
                if new_block[i-1] == '#':
                    continue
                elif new_block[i-1] == '?':
                    new_block[i-1] = '.'

            end_i = i + search_number

            if end_i < len(new_block):
                if new_block[end_i] == '#':
                    continue
                elif new_block[end_i] == '?':
                    new_block[end_i] = '.'

            new_blocks = list(blocks)
            new_blocks[block_number] = "".join(new_block)

            new_s = '.'.join(new_blocks)
            
            ret += work((new_s, goal), idx+1)

    return set(ret)

with open('2023/12/12.txt') as f:
    content = f.readlines()

content = [split(x.strip()) for x in content]

print(max([x.count('?') for x, _ in content]))

total = 0
for line in tqdm(content):
    res = work(line)

    total += len(res)

print(f"number of work calls: {calls}")

print(total)