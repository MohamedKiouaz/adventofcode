with open('6/6.txt') as f:
    content = f.readlines()

content = [x.strip().lower() for x in content]

duration_str, distance_str = content

duration_str = duration_str.replace('time:', '')
distance_str = distance_str.replace('distance:', '')

durations = duration_str.split(' ')
durations = [x for x in durations if x]
durations = [int(x) for x in durations]

distances = distance_str.split(' ')
distances = [x for x in distances if x]
distances = [int(x) for x in distances]

print(durations)
print(distances)

def d(h, d):
    return h * (d - h)

result = 1
for duration, distance in zip(durations, distances):
    ways = 0
    for h in range(0, duration):
        if d(h, duration) > distance:
            ways += 1
    result *= ways

print(result)
