import sys

raw_data = sys.argv[-1]

with open(raw_data, 'r') as inp_data:
    content = inp_data.read().strip()

grid = []
for line in content.split('\n'):
    grid.append([])
    for cell in line:
        grid[-1].append(cell)

m = len(grid)
n = len(grid[0])

col_for_all_rows = {}
for c in range(n):
    col_for_all_rows[c] = 0

extra_row_after_row_r = []

for r in range(m):
    cnt_glx = 0
    for c in range(n):
        if grid[r][c] == '#':
            cnt_glx += 1
            col_for_all_rows[c] = 1
            
    if cnt_glx == 0:
        extra_row_after_row_r.append(r+1)

extra_col_after_col_c = []
for col, freq in col_for_all_rows.items():
    if not freq:
        extra_col_after_col_c.append(col+1)

#print(extra_row_after_row_r, extra_col_after_col_c)
expanded_grid = []
small_row = float('inf')
add_rows = []
add_cols = []
added_c = 0
added_r = 0
for r in range(m):
    added_c = 0
    if r in extra_row_after_row_r:
        added_r += 999999
        for c in range(n):
            if c in extra_col_after_col_c:
                expanded_grid[-1].append('.')
            expanded_grid[-1].append('.')
    expanded_grid.append([])
    for c in range(n):
        if c in extra_col_after_col_c:
            added_c += 999999
            expanded_grid[-1].append((r+added_r, added_c+c-1))
        if grid[r][c] == '#':
            expanded_grid[-1].append(((r+added_r, c+added_c),grid[r][c]))
        else:
            expanded_grid[-1].append((r+added_r, c+added_c))

for row in expanded_grid:
    small_row = min(len(row), small_row)

expanded_symmetrical_grid = []
r = -1
for row in expanded_grid:
    r += 1
    c = -1
    if len(row) > small_row :
        for i in range(2):
            expanded_symmetrical_grid.append([])
            for col in row:
                c += 1
                if c >= small_row:
                    break
                expanded_symmetrical_grid[-1].append(expanded_grid[r][c])
            c = -1
    else:
        expanded_symmetrical_grid.append(expanded_grid[r])
    
asteroids = []
for r in range(len(expanded_symmetrical_grid)):
    for c in range(len(expanded_symmetrical_grid[r])):
        if len(expanded_symmetrical_grid[r][c]) == 2 and expanded_symmetrical_grid[r][c][1] == '#':
            asteroids.append((r, c))

expanded_symmetrical_grid2 = []
sett = []
asteroids_part2 = []

for row in expanded_symmetrical_grid:
    dont = False
    for row_2 in sett:
        if row == row_2:
            dont= True
            break
    if not dont:
        expanded_symmetrical_grid2.append(row)
    sett.append(row)

sum_of_distances = 0
for i in range(len(asteroids)):
    curr_distance = 0
    for j in range(i, len(asteroids)):
        sum_of_distances += abs(asteroids[i][0] - asteroids[j][0]) + abs(asteroids[i][1] - asteroids[j][1])

print(sum_of_distances) # part1

for i in range(len(expanded_symmetrical_grid2)):
    for j in range(len(expanded_symmetrical_grid2[i])):
        if expanded_symmetrical_grid2[i][j][1] == '#':
            asteroids_part2.append(expanded_symmetrical_grid2[i][j][0])

sum_of_distances2 = 0
for i in range(len(asteroids_part2)):
    curr_distance = 0
    for j in range(i, len(asteroids_part2)):
        sum_of_distances2 += abs(asteroids_part2[i][0] - asteroids_part2[j][0]) + abs(asteroids_part2[i][1] - asteroids_part2[j][1])

print(sum_of_distances2) # part2