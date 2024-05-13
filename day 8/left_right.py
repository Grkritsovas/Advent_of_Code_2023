import re
import sys
from itertools import cycle
from functools import reduce
from math import gcd
def lcm_x_y(a, b):
    return abs(a*b) // gcd(a, b)
# Define a function 'test' that calculates the LCM (Least Common Multiple) of a list of numbers.
def test(nums):
    # Use the 'reduce' function to apply the 'lcm' function cumulatively to the elements of 'nums'.
    return reduce(lambda x, y: lcm_x_y(x, y), nums)

# Read input data from a file
raw_data = sys.argv[-1]
with open(raw_data, "r") as inp_data:
    # Read the entire content of the file
    content = inp_data.read().strip()

# Regular expression to match consecutive 'L' or 'R' characters
pattern = re.compile(r'[LR]+')

# Search for matches in the entire content
matches = re.findall(pattern, content)
if matches:
    # Print all matches found
    for match in matches:
        l_r = match
        break
else:
    print("No match found")

start_of_nodes = 1
for line in l_r.split('\n'):
    start_of_nodes += 1

nodes = []
nodess = {}
#part 2 we use ghost_nodes with different logic to store node info
ghost_nodes = {}
counter_a = 0
i = 0
for line in content.split('\n'):
    if i < start_of_nodes:
        pass
    else:
        line_split = line.split()
        src = line_split[0]
        if src[-1] == 'A':
            for token in line_split:
                if '(' in token:
                    l = token[1:-1]
                if ')' in token:
                    r = token[:-1]
            ghost_nodes[src] = (l, r)

        l = ''
        r = ''
        for token in line_split:
            if '(' in token:
                l = token[1:-1]
            if ')' in token:
                r = token[:-1]
        nodes.append([src, (l, r)])
        nodess[src] = (l, r)
    i += 1
#print(nodes)
src = ''
dest = ''
i = 0
node_idx = 0
steps = 0
looking_for_start = True

while True:
    if node_idx > len(nodes) - 1:
        node_idx = 0
    if i > len(l_r) - 1:
        i = 0

    src = nodes[node_idx][0]

    if steps: 
        if src == dest:
            direction = l_r[i]
            steps += 1
            if direction == 'L':
                dest = nodes[node_idx][1][0]
            else:
                dest = nodes[node_idx][1][1]

            if dest == 'ZZZ':
                break
            i += 1  
    
    if src == 'AAA' and looking_for_start:
        steps = 1
        looking_for_start = False
        direction = l_r[i]
        if direction == 'L':
            dest = nodes[node_idx][1][0]
        else:
            dest = nodes[node_idx][1][1]
            print(src, '->', dest, 'direction: ', direction) 
        i += 1

    node_idx += 1
print(steps)

#part 2
instructions = []
for direction in l_r:
    if direction == 'L':
        instructions.append(0)
    else:
        instructions.append(1)
periods = []
for node in ghost_nodes:
    steps = 0
    start_node = node

    for direction in cycle(instructions):
            node = nodess[node][direction]
            steps += 1
            if node.endswith('Z'):
                periods.append(steps)
                break
result = test(periods)
print(result)