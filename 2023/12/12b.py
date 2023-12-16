from multiprocessing import freeze_support
import numpy as np
from tqdm import tqdm
from itertools import combinations
from concurrent.futures import ProcessPoolExecutor
import math

def ways(N, X):
    return math.comb(N + X - 1, X - 1)

def split(line):
    s, goal = line.split(' ')
    goal = [int(g) for g in goal.split(',')]

    return s, goal

def work(splitted_line):
    s, goal = splitted_line

    # print(s, goal)

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

    if diese_count + question_count == goal_sum and question_count > 0:
        # only one way to do it
        return work((s.replace('?', '#'), goal))
    
    
    ss = s.split('.')
    ss = [x for x in ss if x != '']

    i = 0
    while i < len(ss):
        if '?' in ss[i]:
            break
        elif len(ss[i]) != goal[i]:
            return []
        i += 1

    if question_count == 0:
        ss = [len(x) for x in ss]

        if len(ss) == len(goal) and all([ss[i] == goal[i] for i in range(len(ss))]):
            return [s]
    
    if diese_count == goal_sum and question_count > 0:
        # only one way to do it
        return work((s.replace('?', '.'), goal))
    
    if question_count > 0:
        ret = work((s.replace('?', '.', 1), goal))

        if diese_count < goal_sum:
            ret += work((s.replace('?', '#', 1), goal))

        return ret
    
    return []

def extend(parsed_line):
    s, goal = parsed_line

    # repeat 5 times goal
    goal = [g for _ in range(4) for g in goal]
    # repeat 5 times s with a ? between each
    s = '?'.join([s for _ in range(4)])
    
    return s, goal


if __name__ == '__main__':
    freeze_support()
    with open('2023/12/12.txt') as f:
        content = f.readlines()

    content = [split(x.strip()) for x in content]
    content = [extend(x) for x in content]

    # work(('?'*12, (3, 2, 1)))

    # exit()


    with ProcessPoolExecutor() as exec:
        res = list(tqdm(exec.map(work, content), total=len(content)))

    print(sum([len(x) for x in res]))

    total = 0
    for line in tqdm(content):
        print(line)
        print('number of ? =', line[0].count('?'))
        res = work(line)

        # print(res)
        # print(line, len(res))

        total += len(res)

    print(f"total: {total}")