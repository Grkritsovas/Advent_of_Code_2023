import sys

raw_data = sys.argv[-1]
input_data = open(raw_data, 'r')
lines = input_data.read().split('\n')

def solve(lines):
    #CONSTRAINTS : 12 RED, 13 GREEN, 14 BLUE
    valid_games = set()
    t = 0
    game_pos = []
    power_sum = 0
    sett = []
    for game in lines:
        ignore_this = False
        t += 1
        #split into the different iterations of each game
        red_max_pres = 0
        blue_max_pres = 0
        green_max_pres = 0
        game_snapshots = game.split(';')
        for game_snapshot in game_snapshots:
            colours = {'red': 12, 'blue': 14,'green': 13}
            tokens = game_snapshot.split(' ')
            remove_this_game_id = False
            for i, token in enumerate(tokens):
                if token in colours:
                    if token == 'red':
                        if int(tokens[i-1]) > red_max_pres:
                            red_max_pres = int(tokens[i-1])
                    elif token == 'blue':
                        if int(tokens[i-1]) > blue_max_pres:
                            blue_max_pres = int(tokens[i-1])
                    elif token == 'green':
                        if int(tokens[i-1]) > green_max_pres:
                            green_max_pres = int(tokens[i-1])
                    colours[token] -= int(tokens[i-1])
                    if colours[token] < 0:
                        remove_this_game_id = True
                elif token[:-1] in colours:
                    if token[:-1] == 'red':
                        if int(tokens[i-1]) > red_max_pres:
                            red_max_pres = int(tokens[i-1])
                    elif token[:-1] == 'blue':
                        if int(tokens[i-1]) > blue_max_pres:
                            blue_max_pres = int(tokens[i-1])
                    elif token[:-1] == 'green':
                        if int(tokens[i-1]) > green_max_pres:
                            green_max_pres = int(tokens[i-1])
                    colours[token[:-1]] -= int(tokens[i-1])
                    if colours[token[:-1]] < 0:
                        remove_this_game_id = True
            if remove_this_game_id:
                if t in valid_games:
                    valid_games.remove(t)
                ignore_this = True
            else:
                if not ignore_this:
                    valid_games.add(t)
        power_sum += green_max_pres*blue_max_pres*red_max_pres
        sett.append(green_max_pres)
        sett.append( blue_max_pres)
        sett.append(red_max_pres)

    print(sum(valid_games)-t)#part 1
    print(power_sum)#part 2

if __name__ == "__main__":
    solve(lines)