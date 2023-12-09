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

current = "AAA"

i = 0
while current != "ZZZ":
    index = int(path[i % len(path)] == "R")
    current = map_[current][index]
    i += 1

print(i)