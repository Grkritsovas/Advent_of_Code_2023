import sys
from collections import defaultdict

raw_input = sys.argv[-1]
input_data = open(raw_input, 'r')
lines = input_data.read().split('\n')
#number 1 is destination category, number 2 is source, number 3 is range for both
seed_to_soil_map = []
soil_to_fertilizer_map = []
fertilizer_to_water_map = []
water_to_light_map = []
light_to_temperature_map = []
temperature_to_humidity_map = []
humidity_to_location_map = []
names_vector = {'seed-to-soil': seed_to_soil_map, 'soil-to-fertilizer'
    :soil_to_fertilizer_map, 'fertilizer-to-water':fertilizer_to_water_map,
    'water-to-light': water_to_light_map, 'light-to-temperature':
    light_to_temperature_map, 'temperature-to-humidity': temperature_to_humidity_map,
    'humidity-to-location':humidity_to_location_map}

#construct the arrays
seeds = lines[0].split()[1:]
#part 2 seeds are given as ranges
seeds_ranges = []
for i in range(0, len(seeds), 2):
    seeds_ranges.append((int(seeds[i]), int(seeds[i]) + int(seeds[i+1]) - 1) )
print(seeds_ranges)
i = 0
for line in lines:
    if i == 0:
        i += 1
        continue
    if line == '':
        continue
    line_contents = line.split()
    #print(line_contents)
    if line_contents[0] in names_vector:
        curr_list = names_vector[line_contents[0]]
    else:
        numbers = line.split()
        curr_list.append((int(numbers[0]), int(numbers[1]), int(numbers[2])))

min_distance_destination = float('inf')
for seed in seeds:
    src = int(seed)

    for curr_map in names_vector.values():#iterate over the different maps
        dest_found = False # keep track if we found a mapping for the starting src to dest
        for range_map in curr_map:
            if src >= range_map[1] and src < range_map[1] + range_map[2]: # check if source is in the range of the current map
                dest_2 = range_map[0] # starting range of destination
                src_2 = range_map[1] # starting range of source

                dest = dest_2 - src_2 + src # mapped source->destination will be equal to difference of starting ranges of the 2 plus the src we're looking for

                dest_found = True

            if not dest_found:
                dest = src
        # src_before = src
        src = dest # new source will be where the destination was mapped from the previous source

    if dest < min_distance_destination: # if this final mapping for location is smaller than the previous, update smallest location val
        min_distance_destination = dest

print(min_distance_destination)

#part 2: we first need to constract maps of ranges (low, high) instead of direct maps of locations : (exact) then traverse in reverse to find 
#the smallest available (low) and which initial seed it corresponds to
min_distance_from_range = (float('inf'), float('inf') )
for seed_low, seed_high in seeds_ranges:
    src = (seed_low, seed_high)
    dest = src
    for curr_map in names_vector.values():#iterate over the different maps
        dest_found = False # keep track if we found a mapping for the starting src to dest
        for range_map in curr_map:
            dest_2 = (range_map[0], range_map[0] + range_map[2] - 1)
            src_2 = (range_map[1], range_map[1] + range_map[2] - 1)
            diff = dest_2[0] - src_2[0]
            print(src_2, src)
            if src[0] >= src_2[0] and src[1] < src_2[1]:
                dest = (diff + dest_2[0], diff + dest_2[1])
                dest_found = True
            #elif src[0] >= src_2
            
            if not dest_found:
                dest = src
                print(dest, '!')
        src = dest

    if dest[0] < min_distance_from_range[0]:
        min_distance_from_range = dest

print(min_distance_from_range)
            
