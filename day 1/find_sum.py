import sys
nums = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'zero': '0'}

input_data = sys.argv[-1]
f = open(input_data,'r')
lines = f.read().split('\n')

def solve(lines):
    res_part_1 = 0
    res_part_2 = 0
    digits_part_one = []
    digits_part_two = []
    for line in lines:
        digits_part_one.clear()
        digits_part_two.clear()
        string_num = ''
        for ch in line:
            string_num += ch
            if len(string_num) > 4:
                if string_num[-5:] in nums.keys():
                    digits_part_two.append(nums[string_num[-5:]])
            if len(string_num) > 3:
                if string_num[-4:] in nums.keys():
                    digits_part_two.append(nums[string_num[-4:]])
            if len(string_num) > 2:
                if string_num[-3:] in nums.keys():
                    digits_part_two.append(nums[string_num[-3:]])        
            
            if ch.isdigit():
                digits_part_one.append(ch)
                digits_part_two.append(ch)

        if digits_part_one and digits_part_two:
            res_part_1 += int(digits_part_one[0] + digits_part_one[-1])
            res_part_2 += int(digits_part_two[0] + digits_part_two[-1]) 

    print(res_part_1)
    print(res_part_2)

if __name__ == "__main__":
    solve(lines)
        