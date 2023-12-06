with open('2022/1/1.txt') as f:
    content = f.readlines()

content = [x.strip().lower() for x in content]

elfs = [0]

for line in content:
    if line == '':
        elfs.append(0)

    else:
        elfs[-1] += int(line)

print(elfs)

print(max(elfs))

total = 0
for i in range(3):
    total += max(elfs)
    elfs.remove(max(elfs))

print(total)