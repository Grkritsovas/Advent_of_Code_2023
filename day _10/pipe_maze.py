import sys
from collections import defaultdict
from enum import Enum

raw_data = sys.argv[-1]

with open(raw_data, "r") as inp_data:
    # Read the entire content of the file
    content = inp_data.read().strip()

pipe_2d = []
for line in content.split('\n'):
    pipe_2d.append([])
    for cell in line:
        pipe_2d[-1].append(cell)

directions = { '|': lambda row, col: ((row +1 , col), (row -1, col)), '-': lambda row, col: ((row, col - 1), (row, col +1)),
        'L': lambda row, col: ((row-1, col), (row, col+1)), 'J':lambda row, col: ((row, col-1), (row -1, col )),
        '7': lambda row, col: ((row, col - 1),(row+1, col)), 'F': lambda row, col: ((row +1, col), (row, col + 1))}

m = len(pipe_2d)
n = len(pipe_2d[0])
debug_c = 0
max_visited = set()
for r in range(m):
    for c in range(n):
        if pipe_2d[r][c] == 'S':
            start_coordinates = (r, c)
            for dir in directions.values():#try only going left
                left_r = dir(r, c)[0][0]
                left_c = dir(r, c)[0][1]
                prev_r = left_r
                prev_c = left_c
                right_r = dir(r, c)[1][0]
                right_c = dir(r, c)[1][1]

                next_pos = pipe_2d[left_r][left_c]
                next_pos_right = pipe_2d[right_r][right_c]
                if not (next_pos in directions.keys() and (next_pos_right in directions.keys() )):
                    continue
                visited = set()
                visited.add((r, c))
                
                while next_pos != 'S':
                    visited.add((prev_r, prev_c))
                    if not (next_pos in directions.keys() and( (next_pos_right in directions.keys() or next_pos_right =='S'))):

                        break
                    next_r = directions[pipe_2d[prev_r][prev_c]](prev_r, prev_c)[0][0]
                    next_c = directions[pipe_2d[prev_r][prev_c]](prev_r, prev_c)[0][1]
                    next_pos_right = pipe_2d[directions[pipe_2d[prev_r][prev_c]](prev_r, prev_c)[1][0]][directions[pipe_2d[prev_r][prev_c]](prev_r, prev_c)[1][1]]

                    if (next_r, next_c) in visited:

                        next_pos_right = pipe_2d[next_r][next_c]
                        next_r = directions[pipe_2d[prev_r][prev_c]](prev_r, prev_c)[1][0]
                        next_c = directions[pipe_2d[prev_r][prev_c]](prev_r, prev_c)[1][1]
                        if (next_r, next_c) in visited:
                            break
                    prev_r = next_r
                    prev_c = next_c

                    if next_r < 0 or next_c < 0 or next_r > m - 1 or next_c > n - 1:
                        break
                    next_pos = pipe_2d[next_r][next_c]

                    debug_c += 1
                    visited.add((next_r, next_c))
                    if len(visited) > len(max_visited):
                        max_visited = visited

print(len(max_visited)//2)

class Direction(Enum):
    North = (-1, 0)
    South = (1, 0)
    East = (0, 1)
    West = (0, -1)

opposite_dict = {
    Direction.North: Direction.South,
    Direction.South: Direction.North,
    Direction.East: Direction.West,
    Direction.West: Direction.East
}

def opposite(direction):
    return opposite_dict[direction]

# for each pipe symbol, record the directions where it has openings
pipe_dict = {
    '|': {Direction.North, Direction.South},
    '-': {Direction.East, Direction.West},
    'L': {Direction.North, Direction.East},
    'J': {Direction.North, Direction.West},
    '7': {Direction.South, Direction.West},
    'F': {Direction.South, Direction.East},
}
def neighbour_coordinates(coordinates, direction):
    """
    Given a pair of (row, column) `coordinates`, return the coordinates
    of the neighbouring point in a specific `direction`
    """
    return (
        coordinates[0] + direction.value[0],
        coordinates[1] + direction.value[1]
    )

def start(start_coordinates, pipe_map):
    """
    Given the start coordindates in the pipe map, return the
    actual start symbol (i.e. under 'S') and the two directions
    that can be followed starting from 'S'
    """
    # create a dict that maps a direction to the symbols (pipe shapes)
    # that have openings in that direction
    pipe_symbols_from_direction = {
        direction: {
            symbol
            for symbol, directions in pipe_dict.items()
            if direction in directions
        }
        for direction in Direction
    }
    start_directions = set()
    # for every direction...
    for direction in Direction:
        neighbour_row, neighbour_column = neighbour_coordinates(start_coordinates, direction)
        if neighbour_row < 0 or neighbour_column < 0:
            continue
        try:
            # ... retrieve the neighbouring pipe symbol...
            neighbour = pipe_map[neighbour_row][neighbour_column]
        except IndexError:
            pass
        else:
            if neighbour == '.':
                continue
            # ... and check if the neighbour has an opening
            # towards the current position
            if neighbour in pipe_symbols_from_direction[opposite(direction)]:
                start_directions.add(direction)
    # knowing the two directions that the starting pipe has to link
    # calculate what the starting pipe symbol needs to be
    for symbol, direction_set in pipe_dict.items():
        if direction_set == start_directions:
            start_symbol = symbol
            break
    return start_symbol, start_directions

def follow(start_coordinates, pipe_map):

    """
    Starting from the start coordinates of the pipe map, generate a trail
    of (coordinates, pipe symbol, direction) tuples, following the pipe
    trail until returning to the start coordinates
    """
    start_symbol, directions = start(start_coordinates, pipe_map)
    direction = directions.pop()
    yield start_coordinates, start_symbol, direction
    coordinates = neighbour_coordinates(start_coordinates, direction)
    while coordinates != start_coordinates:
        symbol = pipe_map[coordinates[0]][coordinates[1]]
        # the pipe symbol has openings in two directions
        # remove the direction facing the current symbol (difference/opposite)
        # and retrieve the remaining direction (next/iter)
        direction = next(iter(pipe_dict[symbol].difference({opposite(direction)})))
        yield coordinates, symbol, direction
        coordinates = neighbour_coordinates(coordinates, direction)

def count_inside(start_coordinates, pipe_map):
    # create a dict mapping a row number to the set of columns
    # intersected by the pipe trail
    intersections = defaultdict(set)
    # follow the pipe trail and record all intersections
    for (row, column), symbol, _ in follow(start_coordinates, pipe_map):
        intersections[row].add((column, symbol))
    # for each row, sort the intersections by column
    intersections = {
        row: sorted(row_intersections)
        for row, row_intersections in intersections.items()
    }

    total_inside_count = 0
    # iterate over all rows with intersections
    for row, intersection_line in intersections.items():
        # iterate over all intersections within a row
        # (we will be checking *pairs* of consecutive intersections
        # and add their distance to the "inside" count if they are
        # on the inside of the trail)
        intersection_iter = iter(intersection_line)
        # initial values
        previous_intersection = -1
        previous_symbol = None
        # this boolean keeps track of whether or not we are
        # on the inside of the trail
        inside = False
        inside_count = 0
        while True:
            try:
                intersection, symbol = next(intersection_iter)
            except StopIteration:
                break
            if symbol == '-':
                continue
            if symbol in ('L', 'F'):
                # we have encountered a new "starting" corner
                if inside:
                    inside_count += intersection - previous_intersection - 1
            if symbol in ('|'):
                if inside:
                    inside_count += intersection - previous_intersection - 1
                # flip: we are now on the other side of the trail
                inside = not inside
            if (
                (symbol == 'J' and previous_symbol == 'F') or
                (symbol == '7' and previous_symbol == 'L')
            ):
                # we have encountered a new "ending" corner
                # flip: we are on the other side of the trail
                # *depending* on the previous corner,
                # i.e. depending on whether the edge we have been
                # riding is convex or concave
                inside = not inside
            previous_intersection = intersection
            previous_symbol = symbol
        total_inside_count += inside_count
    return total_inside_count

# Count the cells inside the path defined by max_visited
result = count_inside(start_coordinates, pipe_2d)
print(result)