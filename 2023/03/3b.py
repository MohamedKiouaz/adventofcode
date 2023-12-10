with open('3/3.txt') as f:
    content = f.readlines()

content = [x.strip().lower() for x in content]

print(len(content))

numbers = '0123456789'

def add_mask(m, i, j):
    if i < 0 or i >= len(m):
        return m
    if j < 0 or j >= len(m[i]):
        return m
    
    m[i][j] = '*'

    return m

mask = ['_' * len(k) for k in content]
mask = [list(k) for k in mask]

def check_chars(chars):
    if len(chars) != 3 and len(chars) != 2:
        raise Exception('bad input')
    
    if len(chars) == 2:
        return int(chars[0].isnumeric() or chars[1].isnumeric())
    
    if len(chars) == 3:
        if chars[0].isnumeric() and not chars[1].isnumeric() and chars[2].isnumeric():
            return 2
        if not chars[0].isnumeric() and not chars[1].isnumeric() and not chars[2].isnumeric():
            return 0
        else:
            return 1
        
l = ['1', '_']
for char1 in l:
    for char2 in l:
        for char3 in l:
            print(char1 + char2 + char3, check_chars(char1 + char2 + char3))

def exactly_two(m, i, j):
    if m[i][j] != '*':
        raise Exception('not a gear')
    
    n = 0
    if i - 1 >= 0:
        j_start = max(0, j - 1)
        j_end = min(len(m[i-1]), j + 2)
        
        n += check_chars(m[i-1][j_start:j_end])

    if i + 1 < len(m):
        j_start = max(0, j - 1)
        j_end = min(len(m[i+1]), j + 2)
        
        n += check_chars(m[i+1][j_start:j_end])

    if j - 1 >= 0:
        n += m[i][j-1].isnumeric()
    if j + 1 < len(m[i]):
        n += m[i][j+1].isnumeric()

    return n == 2

for i, e in enumerate(content):
    for j, c in enumerate(e):
        if c == '*' and exactly_two(content, i, j):
            for ii in range(i-1, i+2):
                for jj in range(j-1, j+2):
                    if ii == i and jj == j:
                        continue
                    mask = add_mask(mask, ii, jj)

print(len(mask), len(mask[0]))

for i, k in enumerate(mask):
    print(f'{i:3}' + ''.join(k))

def search_for_gear(content, i, j, final=False):
    if i < 0 or i >= len(content):
        return None
    if j < 0 or j >= len(content[i]):
        return None
    
    if content[i][j] == '*':
        return (i, j)
    
    if final:
        return None
    
    for ii in range(i-1, i+2):
        for jj in range(j-1, j+2):
            if ii == i and jj == j:
                continue
            ret = search_for_gear(content, ii, jj, True)
            if ret is not None:
                return ret
    return None

gears = {}
          
keep = False
for i in range(len(content)):
    if keep:
        gear_coords = gear_coords or search_for_gear(content, i, j)
        gears[gear_coords] = gears.get(gear_coords, []) + [value]

    value = 0
    keep = False
    gear_coords = None
    for j in range(len(content[i])):
        gear_coords = gear_coords or search_for_gear(content, i, j)
        
        if content[i][j] in numbers:
            value = value * 10 + int(content[i][j])
            if mask[i][j] == '*':
                keep = True
        elif value > 0 and keep:
            gears[gear_coords] = gears.get(gear_coords, []) + [value]
            gear_coords = None
            keep = False
            value = 0
        if content[i][j] not in numbers:
            # content should not be kept
            gear_coords = None
            keep = False
            value = 0

total_2 = 0

for gear_coords, values in gears.items():
    if len(values) != 2:
        print('bad gear', gear_coords, values)
        continue

    total_2 += values[0] * values[1]

print(total_2)