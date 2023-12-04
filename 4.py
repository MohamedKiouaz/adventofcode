from functools import reduce

with open('4.txt') as f:
    content = f.readlines()

content = [x.strip().lower() for x in content]


total = 0

def points(n_wins):
    if n_wins == 0:
        return 0
    else:
        return 2 ** (n_wins - 1)

for i in range(10):
    print(i, points(i))

scratchcards = [1] * len(content)
for i, line in enumerate(content):
    card_str, rounds_str = line.split(':')
    card_id = int(card_str.replace('card', '').strip())
    rounds_str = rounds_str.replace('  ', ' ')
    
    win_numbers, draw_numbers = rounds_str.split('|')
    win_numbers = win_numbers.strip().split(' ')
    draw_numbers = draw_numbers.strip().split(' ')

    win_numbers = [int(x) for x in win_numbers]
    draw_numbers = [int(x) for x in draw_numbers]

    wins = [num in draw_numbers for num in win_numbers]

    print(card_id, wins)

    total += points(wins.count(True))

    for j in range(i + 1, i + 1 + wins.count(True)):
        scratchcards[j] += scratchcards[i]


print(total)
print(sum(scratchcards))
