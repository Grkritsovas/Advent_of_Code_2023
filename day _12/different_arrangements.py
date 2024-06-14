import sys
from collections import defaultdict

raw_data = sys.argv[-1]

with open(raw_data, 'r') as inp_data:
    content = inp_data.read().strip()

grid = []
arrangements = []
for row in content.split('\n'):
    grid.append([])
    arrangements.append([])
    row_data = row.split()
    for cell in row_data[0]:
        grid[-1].append(cell)
    for cell in row_data[1].split(','):
        arrangements[-1].append(cell)

choice = ('.', '#')
for r, row in enumerate(grid):
    c = 0
    len_row = len(row)
    for c in range(len_row):
        if grid[r][c] == '?':
            grid[r][c] = choice


def generate_combinations(arr, index=0, current_combination=None):
    if current_combination is None:
        current_combination = []
    
    # Base case: if we've reached the end of the array
    if index == len(arr):
        return [current_combination]
    
    # Check if the current item is a tuple
    if isinstance(arr[index], tuple):
        # Recursive case for tuple: explore both choices
        left_choice = generate_combinations(arr, index + 1, current_combination + [arr[index][0]])
        right_choice = generate_combinations(arr, index + 1, current_combination + [arr[index][1]])
        return left_choice + right_choice
    else:
        # Recursive case for non-tuple: proceed with the single item
        return generate_combinations(arr, index + 1, current_combination + [arr[index]])

total = 0
for r in range(len(grid)):
    curr_arrangement = list(map(int, arrangements[r]))
    combinations = generate_combinations(grid[r])
    curr_add = 0
    for combination in combinations:
        cur_arrangement = curr_arrangement.copy()
        ar = 0
        legit = True
        one_operational = False
        for i in range(len(combination)):
            if ar >= len(cur_arrangement):
                if combination[i] == '.':
                    continue
                else:
                    legit = False
                    break
            if combination[i] == '#':
                one_operational = True
                cur_arrangement[ar] -= 1
                if cur_arrangement[ar] < 0:
                    legit = False
            else:
                if one_operational:
                    ar += 1
                one_operational = False
        if legit:
            for item in cur_arrangement:
                if item != 0:
                    legit = False
            if legit:
                curr_add += 1
                total += 1

print(total)
#this is only part 1 and it is really slow, as it constructs all the possible different arrangements
#while we could optimize by not exploring any further once we're on an arrangement that starts out wrong.