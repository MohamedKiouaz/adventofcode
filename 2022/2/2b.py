with open('2022/2/2.txt') as f:
    games = f.readlines()

games = [x.strip().lower() for x in games]

games = [x.split(' ') for x in games]

def compute_mine(his, status):
    if status == 'y':
        return his

    if status == 'x':
        if his == 'a':
            return 'c'
        elif his == 'b':
            return 'a'
        elif his == 'c':
            return 'b'

    if status == 'z':
        if his == 'a':
            return 'b'
        elif his == 'b':
            return 'c'
        elif his == 'c':
            return 'a'
    
def score(mine):
    if mine == 'a':
        return 1
    elif mine == 'b':
        return 2
    elif mine == 'c':
        return 3
    
total = 0
for his, status in games:
    if status == 'y':
        total += 3
    elif status == 'z':
        total +=  6

    mine = compute_mine(his, status)
    
    total += score(mine)
    
print(total)