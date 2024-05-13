time = [53, 71, 78, 80]
distance = [275, 1181, 1215, 1524]

#best_distance = lambda x: (time[x] // 2) * (time[x] -time[x]//2)

total_ways = 1
for i in range(len(time)):
    curr_t = time[i] // 2
    ways = 0
    while (curr_t) * (time[i] - curr_t) > distance[i]:
        ways += 1
        curr_t -= 1
    curr_t = (time[i] // 2) + 1
    while (curr_t) * (time[i] - curr_t) > distance[i]:
        ways += 1
        curr_t += 1

    total_ways *= ways

print(total_ways)

time = 53717880
distance = 275118112151524
total_ways = 0
curr_t = time // 2

while (curr_t) * (time - curr_t) > distance:
    total_ways += 1
    curr_t -= 1
curr_t = (time // 2) + 1
while (curr_t) * (time - curr_t) > distance:
    total_ways += 1
    curr_t += 1

print(total_ways)
