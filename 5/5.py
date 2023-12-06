from tqdm import tqdm
from functools import reduce
from dataclasses import dataclass

with open('5/5.txt') as f:
    content = f.readlines()

content = [x.strip().lower() for x in content]

seeds = content[0].replace('seeds:', '').strip().split(' ')
seeds = [int(x.strip()) for x in seeds]

@dataclass
class RangeTransform:
    destination: int
    source: int
    r: int

    def __str__(self) -> str:
        return f"{self.source}-{self.source+self.r-1} -({self.destination-self.source})-> {self.destination}-{self.destination+self.r-1}"
    
    def __repr__(self) -> str:
        return self.__str__()

    def split_by_dest(self, dest_number):
        if dest_number <= self.destination or dest_number >= self.destination + self.r:
            return []
        else:
            left_r = dest_number - self.destination
            return [RangeTransform(self.destination, self.source, left_r), RangeTransform(dest_number, self.source + left_r, self.r - left_r)]
    
    def split_by_source(self, source_number):
        if source_number <= self.source or source_number > self.source + self.r:
            return []
        else:
            left_r = source_number - self.source
            return [RangeTransform(self.destination, self.source, left_r), RangeTransform(self.destination + left_r, self.source + left_r, self.r - left_r)]
        
    def is_identity(self):
        return self.destination == self.source
    
    def __eq__(self, __value: object) -> bool:
        return self.destination == __value.destination and self.source == __value.source and self.r == __value.r

class Transform:
    def __init__(self, name):
        self.maps = []
        self.name = name

    def __str__(self) -> str:
        return f"{self.name}: {len(self.maps)}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def apply(self, numbers):
        for number in numbers:
            for map in self.maps:
                if map.source <= number and number < map.source + map.r:
                    yield map.destination + (number - map.source)
                    break
            else:
                yield number

    def inverse(self):
        ret = Transform(f"{self.name} reverted")
        for map in self.maps:
            ret.maps.append(RangeTransform(map.source, map.destination, map.r))
        
        return ret

maps = []
for line in content[1:]:
    if "map" in line:
        map_name = line.split(' ')[0].strip()
        current_map = Transform(map_name)
        maps.append(current_map)
    elif line.count(' ') == 2:
        dest, source, r = line.split(' ')
        dest = int(dest.strip())
        source = int(source.strip())
        r = int(r.strip())
        current_map.maps.append(RangeTransform(dest, source, r))

print(maps)

results = seeds
for map in maps:
    results = list(map.apply(results))

print(results)
print(min(results))

start = 56_560_000
inverted_maps = [x.inverse() for x in maps[::-1]]

print(inverted_maps)

for i in tqdm(range(start, start + 100_000_000)):
    result = [i]
    for map in inverted_maps:
        result = list(map.apply(result))
    
    for seed_index in range(0, len(seeds), 2):
        if seeds[seed_index] <= result[0] and result[0] < seeds[seed_index] + seeds[seed_index+1]:
            print(i, result[0])
            exit()


            