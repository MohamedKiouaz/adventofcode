from tqdm import tqdm

with open('6/6.txt') as f:
    content = f.readlines()

content = [x.strip().lower() for x in content]

duration_str, distance_str = content

duration_str = duration_str.replace('time:', '').replace(' ', '')
distance_str = distance_str.replace('distance:', '').replace(' ', '')

duration = int(duration_str)
distance = int(distance_str)

print(duration)
print(distance)

def d(h, d):
    return h * (d - h)

ways = 0
for h in tqdm(range(0, duration)):
    if d(h, duration) > distance:
        ways += 1

print(ways)