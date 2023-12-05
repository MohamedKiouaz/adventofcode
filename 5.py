from tqdm import tqdm
from functools import reduce
from dataclasses import dataclass

with open('5.txt') as f:
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
        return f"{self.source} (+ {self.r}) -> {self.destination}"
    
    def __repr__(self) -> str:
        return self.__str__()

    def split_by_dest(self, dest_number):
        if dest_number < self.destination or dest_number > self.destination + self.r:
            return []
        else:
            left_r = dest_number - self.destination
            return [RangeTransform(self.destination, self.source, left_r), RangeTransform(dest_number, self.source + left_r, self.r - left_r)]
    
    def split_by_source(self, source_number):
        if source_number < self.source or source_number > self.source + self.r:
            return []
        else:
            left_r = source_number - self.source
            return [RangeTransform(self.destination, self.source, left_r), RangeTransform(self.destination + left_r, self.source + left_r, self.r - left_r)]
        
    def __add__(self, other, level = 0):
        if level == 3:
            return []
        
        print(f'add {level}', self, other)

        if self.destination == other.source and self.r == other.r:
            print('same')
            return [RangeTransform(other.destination, self.source, self.r)]
        
        if self.destination + self.r <= other.source or other.source + other.r <= self.destination:
            print('no overlap')
            return [self]
        
        my_ranges = self.split_by_dest(max(self.destination, other.source))
        my_ranges += self.split_by_dest(min(self.destination + self.r, other.source + self.r))

        other_ranges = other.split_by_source(max(self.destination, other.source))
        other_ranges += other.split_by_source(min(self.destination + self.r, other.source + other.r))

        L = []

        for my_range in my_ranges:
            for other_range in other_ranges:
                if my_range.r != 0 and other_range.r != 0:
                    #L.extend(my_range + other_range)
                    L.extend(my_range.__add__(other_range, level + 1))

        L = [x for x in L if x]

        ret = []
        for x in L:
            if x not in ret and not x.r == 0:
                ret.append(x)
        return ret
    
    def __eq__(self, __value: object) -> bool:
        return self.destination == __value.destination and self.source == __value.source and self.r == __value.r

print(RangeTransform(0, 0, 300))
print(RangeTransform(10, 10, 10))
print("Sum", RangeTransform(15, 0, 15) + RangeTransform(10, 5, 35))

exit()     

print(RangeTransform(5, 0, 15))
print(RangeTransform(100, 10, 10))
print("Sum", RangeTransform(5, 0, 15) + RangeTransform(100, 10, 10))

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

    def __add__(self, other):
        new_map = Transform(f"{self.name} + {other.name}")
        new_map.maps = self.maps
        for other_map in other.maps:
            for map in new_map.maps:
                if map.destination == other_map.source:
                    map.destination = other_map.destination
                    map.r += other_map.r
                    break
        return new_map

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

min_ = 1e10
for i in tqdm(range(0, len(seeds), 2)):
    for seed in range(seeds[i], seeds[i+1]):
        result = [seed]
        
        for map in maps:
            result = map.apply(result)
        
        min_ = min(min_, min(list(result)))

        
