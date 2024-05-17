import sys

raw_data = sys.argv[-1]
input_data = open(raw_data, 'r')
lines_list = input_data.read().strip().split('\n')
grid = []
for line in lines_list:
    row = []
    for ch in line:
        row.append(ch)
    grid.append(row)
print(grid)
n, m = len(grid), 100
by_grid = {}
t = 0
while t < 10**9:
    t += 1
        
    j = 0
    last_pos = []
        
    while j < m:# North
        i = 0
        last_pos.clear()
        cell_blocked = True
        while i < n:
            if grid[i][j] == '.': # cell is empty
                last_pos.append(i) # append the row position on a stack
                cell_blocked = True # set boolean val to True so when we find a #(block-rock) we know we need to clear the stack first time we encounter it
            elif grid[i][j] == '#': # cell is blocked
                if cell_blocked:
                    cell_blocked = False
                    last_pos.clear()     
            elif grid[i][j] == 'O': # cell is a round rock
            # Scroll the '0' (round rock) to the last available position found and make its previous position empty ('.')
                if last_pos:
                    grid[last_pos.pop(0)][j] = 'O'
                    last_pos.append(i)         
                    grid[i][j] = '.'
            i += 1
        j += 1
    #part one
    if t == 1:
        res_part_one = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'O':
                    res_part_one += n - i
        print(res_part_one)
    i = 0
        
    while i < n:# West
        j = 0
        last_pos.clear()
        cell_blocked = True
        while j < m:
            if grid[i][j] == '.': # cell is empty
                last_pos.append(j) # append the row position on a stack
                cell_blocked = True # set boolean val to True so when we find a #(block-rock) we know we need to clear the stack first time we encounter it
            elif grid[i][j] == '#': # cell is blocked
                if cell_blocked:
                    cell_blocked = False
                    last_pos.clear()
            elif grid[i][j] == 'O': # cell is a round rock
                # Scroll the '0' (round rock) to the last available position found and make its previous position empty ('.')
                if last_pos:
                    grid[i][last_pos.pop(0)] = 'O'
                    last_pos.append(j)
                    grid[i][j] = '.'
            j += 1
        i += 1
    j = 0
        
    while j < m:# South
        i = n-1
        last_pos.clear()
        cell_blocked = True
        while i >= 0:
            if grid[i][j] == '.': # cell is empty
                last_pos.append(i) # append the row position on a stack
                cell_blocked = True # set boolean val to True so when we find a #(block-rock) we know we need to clear the stack first time we encounter it
            elif grid[i][j] == '#': # cell is blocked
                if cell_blocked:
                    cell_blocked = False
                    last_pos.clear()
            elif grid[i][j] == 'O': # cell is a round rock
                # Scroll the '0' (round rock) to the last available position found and make its previous position empty ('.')
                if last_pos:
                    grid[last_pos.pop(0)][j] = 'O'
                    last_pos.append(i)
                    grid[i][j] = '.'
            i -= 1
        j += 1
    i = 0
        
    while i < n:# East
        j = m - 1
        last_pos.clear()
        cell_blocked = True
        while j >=0:
            if grid[i][j] == '.': # cell is empty
                last_pos.append(j) # append the row position on a stack
                cell_blocked = True # set boolean val to True so when we find a #(block-rock) we know we need to clear the stack first time we encounter it
            elif grid[i][j] == '#': # cell is blocked
                if cell_blocked:
                    cell_blocked = False
                    last_pos.clear()
            elif grid[i][j] == 'O': # cell is a round rock
                # Scroll the '0' (round rock) to the last available position found and make its previous position empty ('.')
                if last_pos:
                    grid[i][last_pos.pop(0)] = 'O'
                    last_pos.append(j)
                    grid[i][j] = '.'
            j -= 1
        i += 1

    Gh = tuple(tuple(row) for row in grid)
    if Gh in by_grid:
        cycle_length = t-by_grid[Gh]
        amt = (10**9-t)//cycle_length
        t += amt * cycle_length
    by_grid[Gh] = t

res = 0
for i in range(n):
    for j in range(m):
        if grid[i][j] == 'O':
            res += n - i


print(res)
#print('\n'.join(map(str,(''.join(g) for g in grid))))
