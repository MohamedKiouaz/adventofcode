with open('1a.txt') as f:
    content = f.readlines()

content = [x.strip().lower() for x in content]

numbers = '0123456789'

new_content = []
for line in content:
    new_content.append(''.join([c for c in line if c in numbers]))

total = 0
for line in new_content:
    total += int(line[0]) * 10 + int(line[-1])

print(total)

full_name_numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

new_content = []
for line in content:
    for i, full_name_number in enumerate(full_name_numbers):
        line = line.replace(full_name_number, full_name_number + str(i + 1) + full_name_number)

    new_content.append(''.join([c for c in line if c in numbers]))

total = 0
for line in new_content:
    total += int(line[0]) * 10 + int(line[-1])

print(total)

