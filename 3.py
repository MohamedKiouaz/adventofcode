with open('3.txt') as f:
    content = f.readlines()

content = [x.strip().lower() for x in content]

print(len(content))

# print only the unique chars
print(set(''.join(content)))

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

print(len(mask), len(mask[0]))

for i, e in enumerate(content):
    for j, c in enumerate(e):
        if c not in numbers and c != '.':
            mask = add_mask(mask, i-1, j)
            mask = add_mask(mask, i+1, j)
            mask = add_mask(mask, i, j-1)
            mask = add_mask(mask, i, j+1)
            mask = add_mask(mask, i-1, j-1)
            mask = add_mask(mask, i-1, j+1)
            mask = add_mask(mask, i+1, j-1)
            mask = add_mask(mask, i+1, j+1)

print(len(mask), len(mask[0]))

for i, k in enumerate(mask):
    print(f'{i:3}' + ''.join(k))
          
total = 0
keep = False
for i in range(len(content)):
    if keep:
        total += value
    value = 0
    keep = False
    for j in range(len(content[i])):
        if content[i][j] in numbers:
            value = value * 10 + int(content[i][j])
            if mask[i][j] == '*':
                keep = True
        elif value > 0 and keep:
            if i >= 130:
                print(value)
            total += value
            value = 0
            keep = False
        if content[i][j] not in numbers:
            # content should not be kept
            keep = False
            value = 0

print(total)