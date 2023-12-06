from functools import reduce

with open('2.txt') as f:
    content = f.readlines()

content = [x.strip().lower() for x in content]

games = {}

for line in content:
    game_str, rounds_str = line.split(':')
    game_id = int(game_str.replace('game', '').strip())
    rounds_str = rounds_str.split(';')
    rounds = []
    for round_str in rounds_str:
        balls = {}
        for ball_str in round_str.split(','):
            ball_str = ball_str.strip()
            ball_number, ball_color = ball_str.split(' ')
            ball_number = int(ball_number.strip())
            ball_color = ball_color.strip()
            balls[ball_color] = ball_number
        rounds.append(balls)
    games[game_id] = rounds

requirements = {'red': 12, 'green': 13, 'blue': 14}

total = 0

for game_id, rounds in games.items():
    rounds_ok = True
    for round in rounds:
        if not all([round.get(ball_color, 0) <= ball_number for ball_color, ball_number in requirements.items()]):
            rounds_ok = False
            break
    if rounds_ok:
        total += game_id

print(total)

total_power = 0
for game_id, rounds in games.items():
    best = {'red': 0, 'green': 0, 'blue': 0}
    for round in rounds:
        for ball_color, ball_number in round.items():
            if ball_number > best[ball_color]:
                best[ball_color] = ball_number

    power = reduce(lambda x, y: x * y, best.values())
    total_power += power

print(total_power)