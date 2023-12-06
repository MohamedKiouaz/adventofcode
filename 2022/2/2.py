with open('2022/2/2.txt') as f:
    games = f.readlines()

games = [x.strip().lower() for x in games]

games = [x.replace('x', 'a').replace('y', 'b').replace('z', 'c') for x in games]

games = [x.split(' ') for x in games]

def win(his, mine):
    if his == 'a':
        return mine == 'b'
    elif his == 'b':
        return mine == 'c'
    elif his == 'c':
        return mine == 'a'
    
def score(mine):
    if mine == 'a':
        return 1
    elif mine == 'b':
        return 2
    elif mine == 'c':
        return 3
    
total = 0
for his, mine in games:
    total += score(mine)
    if mine == his:
        total += 3
    elif win(his, mine):
        total += 6
    
print(total)