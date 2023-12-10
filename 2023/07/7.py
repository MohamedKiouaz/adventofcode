from functools import cmp_to_key

with open('2023/7/7.txt') as f:
    content = f.readlines()

content = [x.strip().lower() for x in content]
content = [x.split(" ") for x in content]

bids = {}
for card, bid in content:
    bids[card] = (bid)

# sort in this order A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2
def value_of_a_card(card):
    if card[0] == 'a':
        return 14
    elif card[0] == 'k':
        return 13
    elif card[0] == 'q':
        return 12
    elif card[0] == 'j':
        return 11
    elif card[0] == 't':
        return 10
    else:
        return int(card[0])

def value(cards):
    numbers = sorted(list(set(sorted([cards.count(card) for card in cards]))), reverse=True)

    #print(numbers)

    if len(set(cards)) == 1:
        return 6
    elif len(set(cards)) == 2:
        if numbers == [4, 1]:
            return 5
        else:
            return 4
    elif len(set(cards)) == 3:
        if numbers[0] == 3:
            return 3
        elif numbers[0] == 2:
            return 2
    elif len(set(cards)) == 4:
        return 1
    
    return 0

value_to_str =  ["High Card", "Pair", "Two Pairs", "Three of a Kind", "Full House", "Four of a Kind", "Five of a kind"]

def score(card):
    ret = value(card) * 100 ** 7
    for i in range(5):
        ret += value_of_a_card(card[i]) * 100 ** (6 - i)
    return ret

hands = [hand for hand, _ in content]

hands.sort(key=cmp_to_key(lambda x, y: score(x) - score(y)))

total = 0
for i, hand in enumerate(hands):
    print(f"{i + 1:4} {hand} {value_to_str[value(hand)]:15} {bids[hand]:5}")
    total += int(bids[hand]) * (i + 1)

print(total)