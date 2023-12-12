import numpy as np
from tqdm import tqdm
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor

def split(line):
    s, goal = line.split(' ')
    goal = [int(g) for g in goal.split(',')]

    return s, goal

def work(splitted_line):
    s, goal = splitted_line

    diese_count = s.count('#')
    point_count = s.count('.')
    question_count = s.count('?')
    goal_sum = sum(goal)
    
    if diese_count > goal_sum:
        # too many diese
        return []
    
    if diese_count + question_count < goal_sum:
        # no path to goal
        return []
    
    if question_count == 0:
        ss = s.split('.')
        ss = [len(x) for x in ss if x != '']
        # print(s, ss)

        if len(ss) == len(goal) and all([ss[i] == goal[i] for i in range(len(ss))]):
            return [s]
    
    if diese_count == goal_sum and question_count > 0:
        return work((s.replace('?', '.'), goal))
    
    if question_count > 0:
        ret = work((s.replace('?', '.', 1), goal))

        if diese_count < goal_sum:
            ret += work((s.replace('?', '#', 1), goal))

        return ret
    
    return []

with open('2023/12/12.txt') as f:
    content = f.readlines()

content = [split(x.strip()) for x in content]

total = 0
for line in tqdm(content):
    res = work(line)

    # print(res)
    # print(line, len(res))

    total += len(res)

print(total)