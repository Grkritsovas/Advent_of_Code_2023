import sys
from collections import defaultdict()

raw_data = sys.argv[-1]
input_data = open(raw_data, 'r')
res = 0
hashmap = defaultdict(int)

for i, game in enumerate(input_data.read().split('\n')):
    if game == '':
        continue
    hashmap[i] += 1
    winning_numbers, my_numbers = game.split('|')
    winning_numbers = winning_numbers.split()
    my_numbers = my_numbers.split()
    game_points = 0
    matches = 0
    for num_w in winning_numbers:
        if not num_w.isdigit():
            continue
        for num_m in my_numbers:
            if num_w == num_m:
                matches += 1
            if num_m == num_w and not game_points:
                game_points = 1
            elif num_m == num_w:
                game_points *= 2

    for j in range(matches):
        hashmap[i+1+j] += hashmap[i]

print(res)
print(sum(hashmap.values()))


