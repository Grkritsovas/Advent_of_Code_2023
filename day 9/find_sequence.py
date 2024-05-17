import sys
from collections import deque

raw_data = sys.argv[-1]
with open(raw_data, "r") as inp_data:
    # Read the entire content of the file
    content = inp_data.read().strip()

histories = []
for line in content.split('\n'):
    histories.append(line)

total_sum = 0
differences_part_2 = []

for history in histories:#sequences
    nums = history.split()
    #initialize the diff to be the initial sequence
    diff_from_prev_seq = [nums]
    diff_from_prev_seq_part_2 = []
    #counter so that the difference-sequences are calculated by 1 less length each time
    c = 0
    while any(x != 0 for x in diff_from_prev_seq[-1]):#keep looping while there is a 0 present in the difference-sequence
        diff_from_prev_seq.append([])#this is a placeholder for each sequence of differences from the last to be placed in
        
        for i in range(1, len(nums)  - c ):
            #constracting the next diff seq by substracting the previous diff seq values 1 by 1
            diff_from_prev_seq[-1].append(int(diff_from_prev_seq[-2][i])- int(diff_from_prev_seq[-2][i-1]))

        c += 1
    
    add_to_level_up = 0#for part 1 where we add to the end
    abstract_to_level_up = 0#for part 2 where we substract from the beginning
    for i in range(len(diff_from_prev_seq) - 1, -1, -1):#traverse in reverse order to go from the all 0's sequence up until the initial
        add_to_level_up += int(diff_from_prev_seq[i][-1])
        diff_from_prev_seq_part_2.append(int(diff_from_prev_seq[i][0]) - abstract_to_level_up)
        abstract_to_level_up = diff_from_prev_seq_part_2[-1]

    total_sum += add_to_level_up
    #add the last extrapolated item in the list to sum them all up after(we could also just calculate this as a sum like with part 1)
    differences_part_2.append(diff_from_prev_seq_part_2[-1])
print(total_sum)
print(sum(differences_part_2))