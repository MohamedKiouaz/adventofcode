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
    
    def merge(self, other):
        if self.source == other.source and self.destination == other.destination:
            return RangeTransform(other.destination, self.source, max(self.r, other.r))
        elif self.destination - self.source == other.destination - other.source and self.source + self.r >= other.source:
            source = min(self.source, other.source)
            dest = min(self.destination, other.destination)
            r = max(self.r, other.r)
            return RangeTransform(dest, source, r)
        else:
            return None
        
    def is_identity(self):
        return self.destination == self.source
        
    def stack(self, other):
        if self.destination == other.source and self.r == other.r:
            return [RangeTransform(other.destination, self.source, self.r)]
        
        if other.is_identity():
            return [self]

        if self.destination + self.r <= other.source or other.source + other.r <= self.destination:
            #print('no overlap')
            return [self]
        
        print(f'stack', self, "/", other)
        
        my_ranges = self.split_by_dest(max(self.destination, other.source))
        my_ranges += self.split_by_dest(min(self.destination + self.r, other.source + self.r))

        other_ranges = other.split_by_source(max(self.destination, other.source))
        other_ranges += other.split_by_source(min(self.destination + self.r, other.source + other.r))

        dup_ranges = []

        for my_range in my_ranges:
            for other_range in other_ranges:
                if my_range.r != 0 and other_range.r != 0:
                    dup_ranges.extend(my_range.stack(other_range))

        dup_ranges = [x for x in dup_ranges if x]

        unique_ranges = []
        for x in dup_ranges:
            if x not in unique_ranges and not x.r == 0:
                unique_ranges.append(x)

        print(unique_ranges)

        return unique_ranges
    
    def __eq__(self, __value: object) -> bool:
        return self.destination == __value.destination and self.source == __value.source and self.r == __value.r

# test split
# print(RangeTransform(0, 0, 10).split_by_dest(5))
# print(RangeTransform(0, 0, 10).split_by_dest(15))
# print(RangeTransform(0, 0, 10).split_by_dest(0))

# print(RangeTransform(0, 0, 10).split_by_source(5))
# print(RangeTransform(0, 0, 10).split_by_source(15))
# print(RangeTransform(0, 0, 10).split_by_source(0))

# print("Sum", RangeTransform(15, 0, 15) + RangeTransform(10, 5, 35))
# print(RangeTransform(15, 0, 15))
# print(RangeTransform(10, 5, 35))

# print("Sum", RangeTransform(5, 0, 15) + RangeTransform(100, 10, 10))
# print(RangeTransform(5, 0, 15))
# print(RangeTransform(100, 10, 10))

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

    def stack(self, other):
        new_map = Transform(f"{self.name} + {other.name}")

        stacked_transform_ranges = []
        for map in self.maps:
            for other_map in other.maps:
                stacked_transform_ranges.extend(map.stack(other_map))

        stacked_transform_ranges = sorted(stacked_transform_ranges, key=lambda x: x.source)
        
        print(stacked_transform_ranges)

        for range in stacked_transform_ranges:
            if len(new_map.maps) >= 1 and range.merge(new_map.maps[-1]) is not None:
                new_map.maps[-1] = range.merge(new_map.maps[-1])
            else:
                new_map.maps.append(range)

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

a = Transform("a")
a.maps.append(RangeTransform(5, 0, 10))
a.maps.append(RangeTransform(15, 10, 10))
b = Transform("b")
b.maps.append(RangeTransform(1, 0, 20))
b.maps.append(RangeTransform(19, 20, 10))

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

        
