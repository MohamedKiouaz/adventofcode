from tqdm import tqdm
from functools import reduce
from dataclasses import dataclass

with open('5_mini.txt') as f:
    content = f.readlines()

content = [x.strip().lower() for x in content]

seeds = content[0].replace('seeds:', '').strip().split(' ')
seeds = [int(x.strip()) for x in seeds]

@dataclass
class Map:
    bounds = [0]
    offsets = [0]

    def clean(self):
        i = 0
        while i < len(self.bounds) - 1:
            if self.offsets[i] == self.offsets[i+1]:
                del self.bounds[i+1]
                del self.offsets[i+1]
            else:
                i += 1

    def stack(self, other):
        result = Map()
        result.bounds = []
        result.offsets = []

        j = 0
        while j < len(other.bounds):
            i = 0
            while i < len(self.bounds):
                if self.bounds[i] + self.offsets[i] < other.bounds[j]:
                    i += 1
                elif self.bounds[i] + self.offsets[i] == other.bounds[j]:
                    result.bounds.append(self.bounds[i])
                    result.offsets.append(self.offsets[i] + other.offsets[j])
                    i += 1
                else:
                    result.bounds.append(other.bounds[j] - self.offsets[i])
                    result.offsets.append(self.offsets[i] + other.offsets[j])
                    i += 1
            j += 1
        return result


maps = []

for line in content[1:]:
    if 'map' in line:
        if len(maps) > 0:
            maps[-1].clean()
            print(maps[-1].bounds)
            print(maps[-1].offsets)
            print()

        maps.append(Map())
        map = maps[-1]
        map.bounds = [0]
        map.offsets = [0]

    if line.count(' ') == 2:
        dest, source, r = line.split(' ')
        dest = int(dest.strip())
        source = int(source.strip())
        r = int(r.strip())
        
        i = 0
        while i != len(map.bounds) and map.bounds[i] < source:
            i += 1

        if i != len(map.bounds) and map.bounds[i] == source:
            map.offsets[i] = dest - source
        else:
            map.bounds.insert(i, source)
            map.offsets.insert(i, dest-source)

        if i + 1 == len(map.bounds):
            map.bounds.append(source + r)
            map.offsets.append(0)
        else:
            while i != len(map.bounds) and map.bounds[i] < source + r:
                i += 1

print("eaa")
print(maps[0].stack(maps[1]).bounds)
print(maps[0].stack(maps[1]).offsets)

exit()

a = map.offsets("a")
a.maps.append(Rangemap.offsets(5, 0, 10))
a.maps.append(Rangemap.offsets(15, 10, 10))
b = map.offsets("b")
b.maps.append(Rangemap.offsets(1, 0, 20))
b.maps.append(Rangemap.offsets(19, 20, 10))

print(a)
for map in a.maps:
    print(map)

print(b)
for map in b.maps:
    print(map)

print(a.stack(b))
for map in a.stack(b).maps:
    print(map)

exit()

print(maps)

results = seeds
for map in maps:
    results = list(map.apply(results))

print(results)
print(min(results))

final_transfo = reduce(lambda x, y: x.stack(y), maps)
print(final_transfo)

min_ = 1e10
for i in tqdm(range(0, len(seeds), 2)):
    for seed in range(seeds[i], seeds[i+1]):
        result = [seed]
        
        for map in maps:
            result = map.apply(result)
        
        min_ = min(min_, min(list(result)))

        
