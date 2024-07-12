import sys

raw_data = sys.argv[-1]
input_data = open(raw_data, 'r')
lines = input_data.read().split('\n')
def solve(lines):
    engine_scheme_2d = []
    #make the input a 2d table
    for row in lines:
        curr_row = []
        for cell in row:
            curr_row.append(cell)
        engine_scheme_2d.append(curr_row)

    engine_scheme_2d.pop()
    n = len(engine_scheme_2d)
    m = len(engine_scheme_2d[0])

    def has_adj_symbol(i, j):
        if i < n - 1:
            if engine_scheme_2d[i+1][j] != '.' and not engine_scheme_2d[i+1][j].isdigit():
                return (True,engine_scheme_2d[i+1][j])
            elif j < m - 1 and engine_scheme_2d[i+1][j+1] != '.' and not engine_scheme_2d[i+1][j+1].isdigit():
                return (True,engine_scheme_2d[i+1][j+1])
            elif j > 0 and engine_scheme_2d[i+1][j-1] != '.' and not engine_scheme_2d[i+1][j-1].isdigit():
                return (True,engine_scheme_2d[i+1][j-1])
        if i > 0:
            if engine_scheme_2d[i-1][j] != '.' and not engine_scheme_2d[i-1][j].isdigit():
                return (True,engine_scheme_2d[i-1][j])
            elif j < m - 1 and engine_scheme_2d[i-1][j+1] != '.' and not engine_scheme_2d[i-1][j+1].isdigit():
                return (True,engine_scheme_2d[i-1][j+1])
            elif j > 0 and engine_scheme_2d[i-1][j-1] != '.' and not engine_scheme_2d[i-1][j-1].isdigit():
                return (True,engine_scheme_2d[i-1][j-1])
        
        if j < m - 1 and engine_scheme_2d[i][j+1] != '.' and not engine_scheme_2d[i][j+1].isdigit():
            return (True,engine_scheme_2d[i][j+1])
        elif j > 0 and engine_scheme_2d[i][j-1] != '.' and not engine_scheme_2d[i][j-1].isdigit():
            return (True, engine_scheme_2d[i][j-1])
        return False
    
    number_sum = 0
    number = []
    numbers = []
    numbers_adj_to_asterisk = []
    valid_gears = []
    adj_asterisk = False
    asterisks_coord = []
    for i in range(n):
        number.clear()
        in_number = False
        count_this_number = False
        number = []
        for j in range(m):
            if engine_scheme_2d[i][j] == '*':
                asterisks_coord.append((i,j))
            if not engine_scheme_2d[i][j].isdigit() and in_number or j == m-1 and in_number:
                if count_this_number:
                    curr_number = ''
                    while number:
                        curr_number += number.pop(0)
                    if j == m-1 and engine_scheme_2d[i][j].isdigit():
                        curr_number += engine_scheme_2d[i][j]
                        start_j, end_j = j-len(curr_number)+1, j
                    else:
                        start_j, end_j = j-len(curr_number), j-1
                    number_sum += int(curr_number)
                    if adj_asterisk:
                        numbers_adj_to_asterisk.append([(i, curr_number),(start_j, end_j)])
                
                else:
                    number.clear()
                count_this_number = False
                in_number = False
                adj_asterisk = False

            if engine_scheme_2d[i][j].isdigit():
                in_number = True
                if has_adj_symbol(i, j):
                    if has_adj_symbol(i,j)[1] == '*':
                        adj_asterisk = True
                    count_this_number = True
            if in_number:
                number.append(engine_scheme_2d[i][j])

    print(number_sum)
    #print(numbers_adj_to_asterisk)

    def adj_cells(i, j, ast_i, ast_j):
        if ast_i in range(max(0, i-1), min(n, i+1)+1) and ast_j in range(max(0, j-1), min(m, j+1)+1):
            return True

    #part 2
    duplets = []

    for ast_i, ast_j in asterisks_coord:
        adj = 0
        curr = []
        for num_i_and_number, num_j_start_end in numbers_adj_to_asterisk:
            include = False
            num_i = num_i_and_number[0]
            num_j_start, num_j_end = num_j_start_end[0], num_j_start_end[1]

            if num_i - ast_i > 1:
                break
            for num_j in range(num_j_start, num_j_end+1):
                if adj_cells(num_i, num_j, ast_i, ast_j):
                    include = True

            if include:
                adj += 1
                curr.append(num_i_and_number[1])

        if adj == 2:
            duplets.append(curr)
        
    #print(numbers_adj_to_asterisk)
    summ = 0
    for a, b in duplets:
        summ += int(a)*int(b)

    print(summ)

if __name__ == "__main__":
    solve(lines)