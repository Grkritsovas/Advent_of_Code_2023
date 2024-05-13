from collections import defaultdict
import sys

raw_data = sys.argv[-1]
hands = defaultdict()
inp_data = open(raw_data, 'r')
for card_info in inp_data.read().strip().split('\n'):
    card, bid = card_info.split()
    hands[card] = bid

#rules:
def type_cards(cards):
    def is_five_of_a_kind(cards):
        return len(cards) - len(set(cards)) == 4
    def is_four_of_a_kind(cards):
        cnt = {}
        for card in cards:
            cnt[card] = cnt.get(card, 0) + 1
        four = 0
        one = 0
        for val in cnt.values():
            if val == 4:
                four = 4
            elif val == 1:
                one = 1
        return one == 1 and four == 4 and len(set(cards)) == 2
    def is_full_house(cards):
        cnt = {}
        for card in cards:
            cnt[card] = cnt.get(card, 0) + 1
        three = 0
        two = 0
        for val in cnt.values():
            if val == 3:
                three = 3
            elif val == 2:
                two = 2
        return three == 3 and two == 2 and len(set(cards)) == 2
    def is_three_of_a_kind(cards):
        cnt = {}
        for card in cards:
            cnt[card] = cnt.get(card, 0) + 1
        three = 0
        for val in cnt.values():
            if val == 3:
                three = 3
                break
        
        return three == 3 and len(set(cards)) == 3
    def is_two_pair(cards):
        cnt = {}
        for card in cards:
            cnt[card] = cnt.get(card, 0) + 1
        one_two = 0
        two_two = 0
        for val in cnt.values():
            if val == 2 and one_two:
                two_two = 2
            if val == 2 and not one_two:
                one_two = 2
            
        return one_two == 2 and two_two == 2 and len(set(cards)) == 3
    def is_one_pair(cards):
        cnt = {}
        for card in cards:
            cnt[card] = cnt.get(card, 0) + 1
        pair = 0
        for val in cnt.values():
            if val == 2:
                pair = 2
            
        return pair == 2 and len(set(cards)) == 4
    
    if is_five_of_a_kind(cards):
        return 7
    elif is_four_of_a_kind(cards):
        return 6
    elif is_full_house(cards):
        return 5
    elif is_three_of_a_kind(cards):
        return 4
    elif is_two_pair(cards):
        return 3
    elif is_one_pair(cards):
        return 2
    else:
        return 1

def cards_values(cards_list):
    values = {'A': 12, 'K': 11, 'Q': 10, 'J': 0, 'T': 9, '9': 8, '8': 7, '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1}
    cards_ranking = defaultdict()

    for i in range(len(cards_list)):
        if 'J' not in cards_list[i]:
            cards_ranking[cards_list[i]] = type_cards(cards_list[i])*1000000000000 + values[cards_list[i][0]]*1500000000
        else:
            cards_ranking[cards_list[i]] = joker_adjust_type(cards_list[i])*1000000000000 + values[cards_list[i][0]]*1500000000

    for i in range(len(cards_list)):
        for j in range(len(cards_list)):
            if cards_list[i][1] != cards_list[j][1]:
                cards_ranking[cards_list[i]] += values[cards_list[i][1]]*1500000
                break
    for i in range(len(cards_list)):
        for j in range(len(cards_list)):
            if cards_list[i][2] != cards_list[j][2]:
                cards_ranking[cards_list[i]] += values[cards_list[i][2]]*15000
                break
    for i in range(len(cards_list)):
        for j in range(len(cards_list)):
            if cards_list[i][3] != cards_list[j][3]:
                cards_ranking[cards_list[i]] += values[cards_list[i][3]]*150
                break
    for i in range(len(cards_list)):
        for j in range(len(cards_list)):
            if cards_list[i][4] != cards_list[j][4]:
                cards_ranking[cards_list[i]] += values[cards_list[i][4]]
                break
    for card in cards_list:
        if card not in cards_ranking:
            cards_ranking[card] = type_cards(card)*1000000000000 + 12
    
    return  {k: v for k, v in cards_ranking.items() if v is not None and k is not None}

def joker_adjust_type(cards):
    values = {'A': 12, 'K': 11, 'Q': 10, 'J': 0, 'T': 9, '9': 8, '8': 7, '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1}
    type_before = type_cards(cards)
    max_type = type_before

    indexes_of_joker = []
    for i, c in enumerate(cards):
        if c == 'J':
            indexes_of_joker.append(i)
    cwjj = list(cards)
    for i in indexes_of_joker:
        for replace_with in values.keys():
            cwj = cwjj.copy()
            for j in range(len(cwj)):
                if cwj[j] == 'J':
                    cwj[j] = replace_with

            if type_cards(''.join(cwj)) > max_type:
                type_now = type_cards(''.join(cwj))
                max_type = type_now

    return max_type

cards_types_rank = defaultdict()
for cards in hands.keys():
    if 'J' in cards:
        cards_types_rank[cards] = joker_adjust_type(cards)
        print('found J', cards_types_rank[cards])
    else:
        cards_types_rank[cards] = type_cards(cards)

cards_with_same_rank = set()

for key, value in cards_types_rank.items():
    cards_with_same_rank.add(key)
        
#print(cards_with_same_rank)
cards_with_same_rank_list = list(cards_with_same_rank)
for card, val in sorted(cards_values(cards_with_same_rank_list).items(), key = lambda x: x[1]):
    print(card, val)

out = []
i = 0
for card, val in sorted(cards_values(cards_with_same_rank_list).items(), key = lambda x: x[1]):
    i += 1
    out.append(int(hands[card])* i)
    #print(card, val, int(hands[card])* i)

print(sum(out))