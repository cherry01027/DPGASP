from xpinyin import Pinyin
from lunardate import LunarDate
import random
import string
import re

seed = []
pinyin_list = []
symbol_list = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}', '[', ']', '|', '\\', ';', ':', '"', "'", '<', '>', ',', '.', '/', '?']
with open("pinyin", 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        line = line.replace('\n','')
        pinyin_list.append(line)

def is_valid_password(password):
    # Check if the password contains lowercase letters, uppercase letters, numbers, and special characters
    has_lowercase = any(char.islower() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in symbol_list for char in password)
    return has_lowercase and has_uppercase and has_digit and has_special

with open("__randompsw__", 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

found = False
while not found:
    # Randomly select 30 rows of data
    selected_lines = random.sample(lines, 30)
    passwords = []
    for line in selected_lines:
        path = line.split('----')
        if len(path) > 1:
            passwords.append(path[1].strip())
    # Concatenate passwords into a complete string
    combined_passwords = ''.join(passwords)
    # Check whether the entire string meets the conditions
    if is_valid_password(combined_passwords):
        found = True
        for line in selected_lines:
            user = []
            path = line.split('----')
            password = path[1]
            user.append(password)
            name = path[2]
            user.append(name)
            id = path[3]
            birthday = id[6:14]
            user.append(birthday)
            seed.append(user)

# Conversion of name formats
def name_transform(name):
    '''
    emample:zhangsan --> 1 zhangsan 2 zs 3 zhangs 4 zsan 5 zhang 6 san
    :param name:Name, convert name into different patterns
    :return:As long as one of them matches, it is considered that the password and name match.
    '''
    name_list = list()
    # 1 full name: zhengyifeng
    p = Pinyin()  # Create a Pinyin instance to convert Chinese characters into Pinyin
    name = p.get_pinyin(name)  # zheng-yi-feng
    s = name.split('-')  # ['zheng','yi','feng']
    name1 = ''.join([i.lower() for i in s])
    # 2 first letter of name: zyf
    name2 = ''.join([i[0].lower() for i in s])
    # 3 family name: zheng
    name3 = s[0]
    # 4 given name: yifeng
    name4 = ''.join([i.lower() for i in s[1::]])
    # 5 full name with its 1st letter capitalized: ZYF
    name5 = ''.join([i.upper() for i in name2])  # A5
    # 6 family name+the 1st letter of the given name: zhengyf
    a1 = ''.join([i[0].lower() for i in s[1::]])
    name6 = name3 + a1
    # 7 family name with its 1st letter capitalized: Zheng
    a2 = name3[0].upper()
    a3 = name3[1::].lower()
    name7 = a2 + a3

    name_list.extend([name1, name2, name3, name4, name5, name6, name7])
    return name_list

# Conversion of birthday formats
def convert_to_lunar(birthday):
    year = int(birthday[:4])
    month = int(birthday[4:6])
    day = int(birthday[6:])
    lunar_date = LunarDate.fromSolarDate(year, month, day)
    lunar_year = lunar_date.year
    lunar_month = lunar_date.month
    lunar_day = lunar_date.day
    lunar_birthday = f"{lunar_year:04d}{lunar_month:02d}{lunar_day:02d}"
    return lunar_birthday

def birthday_transform(birthday):
    birthday_list = list()
    lunar_birthday = convert_to_lunar(birthday)
    year = birthday[0:4]
    month = birthday[4:6]
    day = birthday[6:8]
    # 1 YYYYMMDD:  19870504
    bir1 = year + month + day  # B1
    # 2 YYYYMD: 198754
    if int(month[:1]) != 0 and int(day[:1]) == 0:
        bir2 = year + month + day[1:2]  # B2
    elif int(month[:1]) == 0 and int(day[:1]) != 0:
        bir2 = year + month[1:2] + day
    elif int(month[:1]) == 0 and int(day[:1]) == 0:
        bir2 = year + month[1:2] + day[1:2]
    else:
        bir2 = year + month + day
    # 3  MMDDYYYY: 05041987
    bir3 = month + day + year  # B3
    # 4 MDYYYY: 541987
    if int(month[:1]) != 0 and int(day[:1]) == 0:
        bir4 = month + day[1:2] + year  # B4
    elif int(month[:1]) == 0 and int(day[:1]) != 0:
        bir4 = month[1:2] + day + year
    elif int(month[:1]) == 0 and int(day[:1]) == 0:
        bir4 = month[1:2] + day[1:2] + year
    else:
        bir4 = month + day + year
    # 5 MMDDYYYY: 04051987
    bir5 = day + month + year  # B5
    # 6 DMYYYY: 451987
    if int(month[:1]) != 0 and int(day[:1]) == 0:
        bir6 = day[1:2] + month + year  # B6
    elif int(month[:1]) == 0 and int(day[:1]) != 0:
        bir6 = day + month[1:2] + year
    elif int(month[:1]) == 0 and int(day[:1]) == 0:
        bir6 = day[1:2] + month[1:2] + year  # B6
    else:
        bir6 = day + month + year
    # 7 MMDD: 0504
    bir7 = month + day
    # 8 MD: 54
    if month[:1] != '0' and day[:1] == '0':
        bir8 = month + day[1:2]
    elif month[:1] == '0' and day[:1] != '0':
        bir8 = month[1:2] + day
    elif month[:1] == '0' and day[:1] == '0':
        bir8 = month[1:2] + day[1:2]
    else:
        bir8 = month + day
    # 9 YYYY: 1987
    bir9 = year  # B8
    # 10 YYYYMM: 198705
    bir10 = year + month  # B9
    # 11 YYYYM
    if month[:1] == '0':
        bir11 = year + month[1:2]
    else:
        bir11 = year + month
    # 12 MMYYYY: 051987
    bir12 = month + year  # B10
    # 13 MYYYY: 51987
    if month[:1] == '0':
        bir13 = month[1:2] + year  # B11
    else:
        bir13 = month + year
    # 14 YYMMDD: 870504
    bir14 = year[2:4] + month + day  # B12
    # 15 YYMD: 8754
    if month[:1] != '0' and day[:1] == '0':
        bir15 = year[2:4] + month + day[1:2]
    elif month[:1] == '0' and day[:1] != '0':
        bir15 = year[2:4] + month[1:2] + day
    elif month[:1] == '0' and day[:1] == '0':
        bir15 = year[2:4] + month[1:2] + day[1:2]
    else:
        bir15 = year[2:4] + month + day
    # 16 MMDDYY: 050487
    bir16 = month + day + year[2:4]  # B14
    # 17 MDYY: 5487
    if month[:1] != '0' and day[:1] == '0':
        bir17 = month + day[1:2] + year[2:4]
    elif month[:1] == '0' and day[:1] != '0':
        bir17 = month[1:2] + day + year[2:4]
    elif month[:1] == '0' and day[:1] == '0':
        bir17 = month[1:2] + day[1:2] + year[2:4]
    else:
        bir17 = month + day + year[2:4]
    # 18 DDMMYY: 040587
    bir18 = day + month + year[2:4]  # B16
    # 19 DMYY: 4587
    if month[:1] != '0' and day[:1] == '0':
        bir19 = day[1:2] + month + year[2:4]  # B17
    elif month[:1] == '0' and day[:1] != '0':
        bir19 = day + month[1:2] + year[2:4]
    elif month[:1] == '0' and day[:1] == '0':
        bir19 = day[1:2] + month[1:2] + year[2:4]  # B17
    else:
        bir19 = day + month + year[2:4]
    # Convert to lunar birthday
    year1 = lunar_birthday[0:4]
    month1 = lunar_birthday[4:6]
    day1 = lunar_birthday[6:8]
    bir20 = year1 + month1 + day1
    if month1[:1] != '0' and day1[:1] == '0':
        bir21 = year1 + month1 + day1[1:2]  # B2
    elif month1[:1] == '0' and day1[:1] != '0':
        bir21 = year1 + month1[1:2] + day1
    elif month1[:1] == '0' and day1[:1] == '0':
        bir21 = year1 + month1[1:2] + day1[1:2]
    else:
        bir21 = year1 + month1 + day1
    bir22 = month1 + day1 + year1
    if month1[:1] != '0' and day1[:1] == '0':
        bir23 = month1 + day1[1:2] + year1  # B23
    elif month1[:1] == '0' and day1[:1] != '0':
        bir23 = month1[1:2] + day1 + year1
    elif month1[:1] == '0' and day1[:1] == '0':
        bir23 = month1[1:2] + day1[1:2] + year1
    else:
        bir23 = month1 + day1 + year1
    bir24 = day1 + month1 + year1
    if month1[:1] != '0' and day1[:1] == '0':
        bir25 = day1[1:2] + month1 + year1  # B6
    elif month1[:1] == '0' and day1[:1] != '0':
        bir25 = day1 + month1[1:2] + year1
    elif month1[:1] == '0' and day1[:1] == '0':
        bir25 = day1[1:2] + month1[1:2] + year1
    else:
        bir25 = day1 + month1 + year1
    bir26 = month1 + day1
    if month1[:1] != '0' and day1[:1] == '0':
        bir27 = month1 + day1[1:2]
    elif month1[:1] == '0' and day1[:1] != '0':
        bir27 = month1[1:2] + day1
    elif month1[:1] == '0' and day1[:1] == '0':
        bir27 = month1[1:2] + day1[1:2]
    else:
        bir27 = month1 + day1
    bir28 = year1
    bir29 = year1 + month1
    if month1[:1] == '0':
        bir30 = year1 + month1[1:2]
    else:
        bir30 = year1 + month1
    bir31 = month1 + year1
    if month1[:1] == '0':
        bir32 = month1[1:2] + year
    else:
        bir32 = month1 + year1
    bir33 = year1[2:4] + month1 + day1
    if month1[:1] != '0' and day1[:1] == '0':
        bir34 = year1[2:4] + month1 + day1[1:2]
    elif month1[:1] == '0' and day1[:1] != '0':
        bir34 = year1[2:4] + month1[1:2] + day1
    elif month1[:1] == '0' and day1[:1] == '0':
        bir34 = year1[2:4] + month1[1:2] + day1[1:2]
    else:
        bir34 = year1[2:4] + month1 + day1
    bir35 = month1 + day1 + year1[2:4]
    if month1[:1] != '0' and day1[:1] == '0':
        bir36 = month1 + day1[1:2] + year1[2:4]
    elif month1[:1] == '0' and day1[:1] != '0':
        bir36 = month1[1:2] + day1 + year1[2:4]
    elif month1[:1] == '0' and day1[:1] == '0':
        bir36 = month1[1:2] + day1[1:2] + year1[2:4]
    else:
        bir36 = month1 + day1 + year1[2:4]
    bir37 = day1 + month1 + year1[2:4]
    if month1[:1] != '0' and day1[:1] == '0':
        bir38 = day1[1:2] + month1 + year1[2:4]
    elif month1[:1] == '0' and day1[:1] != '0':
        bir38 = day1 + month1[1:2] + year1[2:4]
    elif month1[:1] == '0' and day1[:1] == '0':
        bir38 = day1[1:2] + month1[1:2] + year1[2:4]
    else:
        bir38 = day1 + month1 + year1[2:4]
    birthday_list.extend([bir1, bir2, bir3, bir4, bir5, bir6, bir7, bir8, bir9,
                          bir10, bir11, bir12, bir13, bir14, bir15, bir16, bir17,
                          bir18, bir19, bir20, bir21, bir22, bir23, bir24, bir25,
                          bir26, bir27, bir28, bir29, bir30, bir31, bir32, bir33,
                          bir34, bir35, bir36, bir37, bir38])
    return birthday_list

# Feature extraction of length
def length_extraction(string, length_count):
    item_length = len(string)
    # If the length already exists in the dictionary, increase the count
    if item_length in length_count:
        length_count[item_length] += 1
    # Otherwise, add the length to the dictionary and set the count to 1
    else:
        length_count[item_length] = 1
    return length_count

# Feature extraction of structure numbers
def strucount_extraction(string, structure_count):
    structure_types = set()
    for char in string:
        # Determine the type of character and add it to the set
        if char.islower():
            structure_types.add('lowercase')
        elif char.isupper():
            structure_types.add('uppercase')
        elif char.isdigit():
            structure_types.add('digit')
        else:
            structure_types.add('special')
    item_structure = len(structure_types)
    if item_structure in structure_count:
        structure_count[item_structure] += 1
    # Otherwise, add the structure number to the dictionary and set the count to 1
    else:
        structure_count[item_structure] = 1
    return structure_count

# Feature extraction of structure
def structure_extraction(string, structure_dict):
    L_dict = {}
    D_dict = {}
    S_dict = {}
    U_dict = {}
    for char in string:
        if char.islower():
            if char in L_dict:
                L_dict[char] += 1
            else:
                L_dict[char] = 1
        elif char.isupper():
            if char in U_dict:
                U_dict[char] += 1
            else:
                U_dict[char] = 1
        elif char.isdigit():
            if char in D_dict:
                D_dict[char] += 1
            else:
                D_dict[char] = 1
        else:
            if char in S_dict:
                S_dict[char] += 1
            else:
                S_dict[char] = 1
    for key in L_dict:
        if key in structure_dict['L']:
            structure_dict['L'][key] += L_dict[key]
        else:
            structure_dict['L'][key] = L_dict[key]

    for key in D_dict:
        if key in structure_dict['D']:
            structure_dict['D'][key] += D_dict[key]
        else:
            structure_dict['D'][key] = D_dict[key]

    for key in S_dict:
        if key in structure_dict['S']:
            structure_dict['S'][key] += S_dict[key]
        else:
            structure_dict['S'][key] = S_dict[key]

    for key in U_dict:
        if key in structure_dict['U']:
            structure_dict['U'][key] += U_dict[key]
        else:
            structure_dict['U'][key] = U_dict[key]
    return structure_dict

# Feature extraction of name
def name_extraction(string, name, name_dict):
    name_contains = False
    name_list = name_transform(name)
    for i in name_list:
        if i in string:
            name_contains = True
            break
    if name_contains:
        name_dict.setdefault(1, 0)
        name_dict[1] += 1
    else:
        name_dict.setdefault(0, 0)
        name_dict[0] += 1
    return name_dict

# Feature extraction of birthday
def birthday_extraction(string, birthday, birthday_dict):
    birthday_contains = False
    birthday_list = birthday_transform(birthday)
    for i in birthday_list:
        if i in string:
            birthday_contains = True
            break
    if birthday_contains:
        birthday_dict.setdefault(1, 0)
        birthday_dict[1] += 1
    else:
        birthday_dict.setdefault(0, 0)
        birthday_dict[0] += 1
    return birthday_dict

# Feature extraction of pinyin
def pinyin_extraction(string, pinyin_list, pinyin_dict):
    pinyin_contains = False
    for i in pinyin_list:
        if i in string:
            pinyin_contains = True
            break
    if pinyin_contains:
        pinyin_dict.setdefault(1, 0)
        pinyin_dict[1] += 1
    else:
        pinyin_dict.setdefault(0, 0)
        pinyin_dict[0] += 1
    return pinyin_dict

# Feature extraction of uppercase
def uppercase_extraction(string, upper_dict):
    upper_contains = False
    for char in string:
        if char.isupper():
            upper_contains = True
            break
    if upper_contains:
        upper_dict.setdefault(1, 0)
        upper_dict[1] += 1
    else:
        upper_dict.setdefault(0, 0)
        upper_dict[0] += 1
    return upper_dict

def symbol_extraction(string, symbol_dict):
    symbol_contains = False
    for i in symbol_list:
        if i in string:
            symbol_contains = True
            break
    if symbol_contains:
        symbol_dict.setdefault(1, 0)
        symbol_dict[1] += 1
    else:
        symbol_dict.setdefault(0, 0)
        symbol_dict[0] += 1
    return symbol_dict

# Initialize an empty dictionary
length_count = {}
structure_count = {}
structure_dict = {'L': {}, 'D': {}, 'S': {}, 'U': {}}
name_dict = {}
birthday_dict = {}
pinyin_dict = {}
upper_dict = {}
symbol_dict = {}
for item in seed:
    length_count = length_extraction(item[0], length_count)
    structure_count = strucount_extraction(item[0], structure_count)
    structure_dict = structure_extraction(item[0], structure_dict)
    name_dict = name_extraction(item[0], item[1], name_dict)
    birthday_dict = birthday_extraction(item[0], item[2], birthday_dict)
    pinyin_dict = pinyin_extraction(item[0], pinyin_list, pinyin_dict)
    upper_dict = uppercase_extraction(item[0], upper_dict)
    symbol_dict = symbol_extraction(item[0], symbol_dict)

def calculate_gini(data_dict):
    # Extract a list of values from a dictionary
    values = list(data_dict.values())
    # Calculate the sum of the dataset
    total = sum(values)
    # Calculate the proportion of each category
    proportions = [value / total for value in values]
    # Calculate Gini index
    gini = 1 - sum(p ** 2 for p in proportions)
    return gini

gini_values = {
    "length": calculate_gini(length_count),
    "strucount": calculate_gini(structure_count),
    "name": calculate_gini(name_dict),
    "birthday": calculate_gini(birthday_dict),
    "pinyin": calculate_gini(pinyin_dict),
    "upper": calculate_gini(upper_dict),
    "symbol": calculate_gini(symbol_dict)
}

def length_strucount_policy(string):
    lens = len(string)
    if lens > 13:
        return string
    else:
        min_value = float('inf')
        difference = 0
        for key in length_count.keys():
            if 8 <= key <= 12 and int(key) > lens:
                # If the value find is smaller than the current minimum value, update the minimum value.
                if length_count[key] < min_value:
                    difference = int(key) - lens
                    min_value = length_count[key]
    structure_types = set()
    for char in string:
        # Determine the type of character and add it to the set
        if char.islower():
            structure_types.add('L')
        elif char.isupper():
            structure_types.add('U')
        elif char.isdigit():
            structure_types.add('D')
        else:
            structure_types.add('S')
    item_structure = len(structure_types)
    min_value = float('inf')
    differ = 0
    for key in structure_count.keys():
        if int(key) > item_structure:
            # If the value find is smaller than the current minimum value, update the minimum value.
            if structure_count[key] < min_value:
                differ = int(key) - item_structure
                min_value = structure_count[key]

    # Record the structure types that do not appear in the string
    missing_types = {'L', 'U', 'D', 'S'} - structure_types
    if difference > 0:
        selected_types = random.sample(missing_types, min(differ, len(missing_types)))
    else:
        selected_types = []
    # Find the smallest key from the sub dictionary corresponding to the key in selected_types
    min_keys = ""  # The string form used to store the minimum value of the key in each str_type
    for str_type in selected_types:  # Iterate through each element str_type in the selected_types list.
        min_keys_in_type = sorted(structure_dict[str_type].keys(), key=lambda x: structure_dict[str_type][x])[
                           :difference]
        min_keys += "".join(map(str, min_keys_in_type))

    # Add the smallest key to the front or end of the string.
    if min_keys is not None:
        if random.choice([True, False]):  # Randomly select and add
            string = min_keys + string
        else:
            string = string + min_keys
    return string

def length_name_policy(name, string):
    lens = len(string)
    count_0 = name_dict.get(0, 0)
    count_1 = name_dict.get(1, 0)
    name_list = name_transform(name)
    if count_0 >= count_1:
        sorted_lengths = sorted([key for key in length_count.keys() if 8 <= key <= 12],
                                key=lambda x: length_count[x],
                                reverse=False)
        min_length = sorted_lengths[0]
        if lens > min_length:
            difflen = lens - min_length
            candidates = [name for name in name_list if len(name) == difflen]
            if candidates:
                chosen_name = random.choice(candidates)
                position = random.choice(["before", "after"])
                if position == "before":
                    return chosen_name + string
                else:
                    return string + chosen_name
            chosen_name = random.choice(name_list)
            position = random.choice(["before", "after"])
            if position == "before":
                return chosen_name + string
            else:
                return string + chosen_name
        else:
            diff = min_length - lens
            candidates = [name for name in name_list if len(name) == diff]
            if candidates:
                chosen_name = random.choice(candidates)
                position = random.choice(["before", "after"])
                if position == "before":
                    return chosen_name + string
                else:
                    return string + chosen_name

            chosen_name = random.choice(name_list)
            position = random.choice(["before", "after"])
            if position == "before":
                return chosen_name + string
            else:
                return string + chosen_name
    else:
        for name in name_list:
            if name in string:
                string = string.replace(name, '')
                sorted_lengths = sorted([key for key in length_count.keys() if 8 <= key <= 12],
                                        key=lambda x: length_count[x],
                                        reverse=False)
                min_length = sorted_lengths[0]
                if lens > min_length:
                    difflen = lens - min_length
                    indices = random.sample(range(len(string)), difflen)
                    string = ''.join([char for i, char in enumerate(string) if i not in indices])
                    return string
                else:
                    diff = min_length - lens
                    selected_dict = random.choice(['L', 'D', 'S', 'U'])
                    sorted_items = sorted(structure_dict[selected_dict].items(), key=lambda x: x[1])
                    new_string = ''.join([item[0] for item in sorted_items[:diff]])
                    insert_index = random.choice([0, len(string)])
                    string = string[:insert_index] + new_string + string[insert_index:]
                    return string
            else:
                sorted_lengths = sorted([key for key in length_count.keys() if 8 <= key <= 12],
                                        key=lambda x: length_count[x],
                                        reverse=False)
                min_length = sorted_lengths[0]
                if lens > min_length:
                    difflen = lens - min_length
                    indices = random.sample(range(len(string)), difflen)
                    string = ''.join([char for i, char in enumerate(string) if i not in indices])
                    return string
                else:
                    diff = min_length - lens
                    selected_dict = random.choice(['L', 'D', 'S', 'U'])
                    sorted_items = sorted(structure_dict[selected_dict].items(), key=lambda x: x[1])
                    new_string = ''.join([item[0] for item in sorted_items[:diff]])
                    insert_index = random.choice([0, len(string)])
                    string = string[:insert_index] + new_string + string[insert_index:]
                    return string

def length_birthday_policy(birthday, string):
    lens = len(string)
    count_0 = birthday_dict.get(0, 0)
    count_1 = birthday_dict.get(1, 0)
    birthday_list = birthday_transform(birthday)
    if count_0 >= count_1:
        sorted_lengths = sorted([key for key in length_count.keys() if 8 <= key <= 12],
                                key=lambda x: length_count[x],
                                reverse=False)
        min_length = sorted_lengths[0]
        if lens > min_length:
            difflen = lens - min_length
            candidates = [birthday for birthday in birthday_list if len(birthday) == difflen]
            if candidates:
                chosen_birthday = random.choice(candidates)
                position = random.choice(["before", "after"])
                if position == "before":
                    return chosen_birthday + string
                else:
                    return string + chosen_birthday
            chosen_birthday = random.choice(birthday_list)
            position = random.choice(["before", "after"])
            if position == "before":
                return chosen_birthday + string
            else:
                return string + chosen_birthday
        else:
            diff = min_length - lens
            candidates = [birthday for birthday in birthday_list if len(birthday) == diff]
            if candidates:
                chosen_birthday = random.choice(candidates)
                position = random.choice(["before", "after"])
                if position == "before":
                    return chosen_birthday + string
                else:
                    return string + chosen_birthday
            chosen_birthday = random.choice(birthday_list)
            position = random.choice(["before", "after"])
            if position == "before":
                return chosen_birthday + string
            else:
                return string + chosen_birthday
    else:
        for birthday in birthday_list:
            if birthday in string:
                string = string.replace(birthday, '')
                sorted_lengths = sorted([key for key in length_count.keys() if 8 <= key <= 12],
                                        key=lambda x: length_count[x],
                                        reverse=False)
                min_length = sorted_lengths[0]
                if lens > min_length:
                    difflen = lens - min_length
                    indices = random.sample(range(len(string)), difflen)
                    string = ''.join([char for i, char in enumerate(string) if i not in indices])
                    return string
                else:
                    diff = min_length - lens
                    selected_dict = random.choice(['L', 'D', 'S', 'U'])
                    sorted_items = sorted(structure_dict[selected_dict].items(), key=lambda x: x[1])
                    new_string = ''.join([item[0] for item in sorted_items[:diff]])
                    insert_index = random.choice([0, len(string)])
                    string = string[:insert_index] + new_string + string[insert_index:]
                    return string
            else:
                sorted_lengths = sorted([key for key in length_count.keys() if 8 <= key <= 12],
                                        key=lambda x: length_count[x],
                                        reverse=False)
                min_length = sorted_lengths[0]
                if lens > min_length:
                    difflen = lens - min_length
                    indices = random.sample(range(len(string)), difflen)
                    string = ''.join([char for i, char in enumerate(string) if i not in indices])
                    return string
                else:
                    diff = min_length - lens
                    selected_dict = random.choice(['L', 'D', 'S', 'U'])
                    sorted_items = sorted(structure_dict[selected_dict].items(), key=lambda x: x[1])
                    new_string = ''.join([item[0] for item in sorted_items[:diff]])
                    insert_index = random.choice([0, len(string)])
                    string = string[:insert_index] + new_string + string[insert_index:]
                    return string

def length_pinyin_policy(string):
    lens = len(string)
    count_0 = pinyin_dict.get(0, 0)
    count_1 = pinyin_dict.get(1, 0)
    if count_0 >= count_1:
        sorted_lengths = sorted([key for key in length_count.keys() if 8 <= key <= 12],
                                key=lambda x: length_count[x],
                                reverse=False)
        min_length = sorted_lengths[0]
        if lens > min_length:
            difflen = lens - min_length
            candidates = [pinyin for pinyin in pinyin_list if len(pinyin) == difflen]
            if candidates:
                chosen_pinyin = random.choice(candidates)
                position = random.choice(["before", "after"])
                if position == "before":
                    return chosen_pinyin + string
                else:
                    return string + chosen_pinyin
            chosen_pinyin = random.choice(pinyin_list)
            position = random.choice(["before", "after"])
            if position == "before":
                return chosen_pinyin + string
            else:
                return string + chosen_pinyin
        else:
            diff = min_length - lens
            candidates = [pinyin for pinyin in pinyin_list if len(pinyin) == diff]
            if candidates:
                chosen_pinyin = random.choice(candidates)
                position = random.choice(["before", "after"])
                if position == "before":
                    return chosen_pinyin + string
                else:
                    return string + chosen_pinyin
            chosen_pinyin = random.choice(pinyin_list)
            position = random.choice(["before", "after"])
            if position == "before":
                return chosen_pinyin + string
            else:
                return string + chosen_pinyin
    else:
        for pinyin in pinyin_list:
            if pinyin in string:
                string = string.replace(pinyin, '')
                sorted_lengths = sorted([key for key in length_count.keys() if 8 <= key <= 12],
                                        key=lambda x: length_count[x],
                                        reverse=False)
                min_length = sorted_lengths[0]
                if lens > min_length:
                    difflen = lens - min_length
                    indices = random.sample(range(len(string)), difflen)
                    string = ''.join([char for i, char in enumerate(string) if i not in indices])
                    return string
                else:
                    diff = min_length - lens
                    selected_dict = random.choice(['L', 'D', 'S', 'U'])
                    sorted_items = sorted(structure_dict[selected_dict].items(), key=lambda x: x[1])
                    new_string = ''.join([item[0] for item in sorted_items[:diff]])
                    insert_index = random.choice([0, len(string)])
                    string = string[:insert_index] + new_string + string[insert_index:]
                    return string
            else:
                sorted_lengths = sorted([key for key in length_count.keys() if 8 <= key <= 12],
                                        key=lambda x: length_count[x],
                                        reverse=False)
                min_length = sorted_lengths[0]
                if lens > min_length:
                    difflen = lens - min_length
                    indices = random.sample(range(len(string)), difflen)
                    string = ''.join([char for i, char in enumerate(string) if i not in indices])
                    return string
                else:
                    diff = min_length - lens
                    selected_dict = random.choice(['L', 'D', 'S', 'U'])
                    sorted_items = sorted(structure_dict[selected_dict].items(), key=lambda x: x[1])
                    new_string = ''.join([item[0] for item in sorted_items[:diff]])
                    insert_index = random.choice([0, len(string)])
                    string = string[:insert_index] + new_string + string[insert_index:]
                    return string

def length_upper_policy(string):
    lens = len(string)
    count_0 = upper_dict.get(0, 0)
    count_1 = upper_dict.get(1, 0)
    if count_0 >= count_1:
        sorted_lengths = sorted([key for key in length_count.keys() if 8 <= key <= 12],
                                key=lambda x: length_count[x],
                                reverse=False)
        min_length = sorted_lengths[0]
        if lens > min_length:
            difflen = lens - min_length
            indices = random.sample(range(len(string)), difflen + 1)
            string = ''.join([char for i, char in enumerate(string) if i not in indices])
            selected_dict = random.choice(['U'])
            sorted_items = sorted(structure_dict[selected_dict].items(), key=lambda x: x[1])
            new_string = sorted_items[0][0]
            insert_index = random.choice([0, len(string)])
            string = string[:insert_index] + new_string + string[insert_index:]
            return string
        else:
            diff = min_length - len(string)
            selected_dict = random.choice(['U'])
            sorted_items = sorted(structure_dict[selected_dict].items(), key=lambda x: x[1])
            new_string = ''.join([item[0] for item in sorted_items[:diff]])
            if diff == len(new_string):
                insert_index = random.choice([0, len(string)])
                string = string[:insert_index] + new_string + string[insert_index:]
                return string
            else:
                diff_1 = diff - len(new_string)
                random_chars = ''.join(random.sample(string, diff_1))
                new_string = new_string + random_chars
                insert_index = random.choice([0, len(string)])
                string = string[:insert_index] + new_string + string[insert_index:]
                return string
    else:
        if any(char.isupper() for char in string):
            string = string.lower()
            sorted_lengths = sorted([key for key in length_count.keys() if 8 <= key <= 12],
                                    key=lambda x: length_count[x],
                                    reverse=False)
            min_length = sorted_lengths[0]
            if lens > min_length:
                difflen = lens - min_length
                indices = random.sample(range(len(string)), difflen)
                string = ''.join([char for i, char in enumerate(string) if i not in indices])
                return string
            else:
                diff = min_length - len(string)
                selected_dict = random.choice(['L', 'D', 'S'])
                sorted_items = sorted(structure_dict[selected_dict].items(), key=lambda x: x[1])
                new_string = ''.join([item[0] for item in sorted_items[:diff]])
                insert_index = random.choice([0, len(string)])
                string = string[:insert_index] + new_string + string[insert_index:]
                return string
        else:
            sorted_lengths = sorted([key for key in length_count.keys() if 8 <= key <= 12],
                                    key=lambda x: length_count[x],
                                    reverse=False)
            min_length = sorted_lengths[0]
            if lens > min_length:
                difflen = lens - min_length
                indices = random.sample(range(len(string)), difflen)
                string = ''.join([char for i, char in enumerate(string) if i not in indices])
                return string
            else:
                diff = min_length - len(string)
                selected_dict = random.choice(['L', 'D', 'S'])
                sorted_items = sorted(structure_dict[selected_dict].items(), key=lambda x: x[1])
                new_string = ''.join([item[0] for item in sorted_items[:diff]])
                insert_index = random.choice([0, len(string)])
                string = string[:insert_index] + new_string + string[insert_index:]
                return string

def length_symbol_policy(string):
    lens = len(string)
    count_0 = symbol_dict.get(0, 0)
    count_1 = symbol_dict.get(1, 0)
    if count_0 >= count_1:
        sorted_lengths = sorted([key for key in length_count.keys() if 8 <= key <= 12],
                                key=lambda x: length_count[x],
                                reverse=False)
        min_length = sorted_lengths[0]
        if lens > min_length:
            difflen = lens - min_length
            indices = random.sample(range(len(string)), difflen+1)
            string = ''.join([char for i, char in enumerate(string) if i not in indices])
            selected_dict = random.choice(['S'])
            sorted_items = sorted(structure_dict[selected_dict].items(), key=lambda x: x[1])
            new_string = sorted_items[0][0]
            insert_index = random.choice([0, len(string)])
            string = string[:insert_index] + new_string + string[insert_index:]
            return string
        else:
            diff = min_length - len(string)
            selected_dict = random.choice(['S'])
            sorted_items = sorted(structure_dict[selected_dict].items(), key=lambda x: x[1])
            new_string = ''.join([item[0] for item in sorted_items[:diff]])
            if diff == len(new_string):
                insert_index = random.choice([0, len(string)])
                string = string[:insert_index] + new_string + string[insert_index:]
                return string
            else:
                diff_1 = diff - len(new_string)
                random_chars = ''.join(random.sample(string, diff_1))
                new_string = new_string + random_chars
                insert_index = random.choice([0, len(string)])
                string = string[:insert_index] + new_string + string[insert_index:]
                return string
    else:
        string = re.sub(r'[^a-zA-Z0-9\s]', '', string)
        sorted_lengths = sorted([key for key in length_count.keys() if 8 <= key <= 12],
                                key=lambda x: length_count[x],
                                reverse=False)
        min_length = sorted_lengths[0]
        if lens > min_length:
            difflen = lens - min_length
            indices = random.sample(range(len(string)), difflen)
            string = ''.join([char for i, char in enumerate(string) if i not in indices])
            return string
        else:
            diff = min_length - len(string)
            selected_dict = random.choice(['L', 'D', 'U'])
            sorted_items = sorted(structure_dict[selected_dict].items(), key=lambda x: x[1])
            new_string = ''.join([item[0] for item in sorted_items[:diff]])
            insert_index = random.choice([0, len(string)])
            string = string[:insert_index] + new_string + string[insert_index:]
            return string

def strucount_policy(string):
    structure_types = set()
    for char in string:
        # Determine the type of character and add it to the set
        if char.islower():
            structure_types.add('L')
        elif char.isupper():
            structure_types.add('U')
        elif char.isdigit():
            structure_types.add('D')
        else:
            structure_types.add('S')
    item_structure = len(structure_types)
    min_value = float('inf')
    difference = 0
    for key in structure_count.keys():
        if int(key) > item_structure:
            if structure_count[key] < min_value:
                difference = int(key) - item_structure
                min_value = structure_count[key]

    # Record the structure types that do not appear in the string
    missing_types = {'L', 'U', 'D', 'S'} - structure_types
    if difference > 0:
        selected_types = random.sample(missing_types, min(difference, len(missing_types)))
    else:
        selected_types = []

    min_key = None
    for str_type in selected_types:
        min_key_in_type = min(structure_dict[str_type].keys(), key=lambda x: structure_dict[str_type][x])
        if min_key is None or min_key_in_type < min_key:
            min_key = min_key_in_type

    if min_key is not None:
        if random.choice([True, False]): 
            string = min_key + string
        else:
            string = string + min_key
    return string

def name_policy(name, string):
    count_0 = name_dict.get(0, 0)
    count_1 = name_dict.get(1, 0)
    name_list = name_transform(name)
    if count_0 >= count_1:
        name = random.choice(name_list)
        position = random.choice(['prefix', 'suffix'])
        if position == 'prefix':
            result = name + string
        else:
            result = string + name
        return result
    else:
        for name in name_list:
            if name in string:
                result = string.replace(name, '')
                return result
        return string

def birthday_policy(birthday, string):
    count_0 = birthday_dict.get(0, 0)
    count_1 = birthday_dict.get(1, 0)
    birthday_list = birthday_transform(birthday)
    if count_0 >= count_1:
        birthday = random.choice(birthday_list)
        position = random.choice(['prefix', 'suffix'])
        if position == 'prefix':
            result = birthday + string
        else:
            result = string + birthday
        return result
    else:
        for birthday in birthday_list:
            if birthday in string:
                result = string.replace(birthday, '')
                return result
        return string

def pinyin_policy(string):
    count_0 = pinyin_dict.get(0, 0)
    count_1 = pinyin_dict.get(1, 0)
    if count_0 >= count_1:
        pinyin = random.choice(pinyin_list)
        position = random.choice(['prefix', 'suffix'])
        if position == 'prefix':
            result = pinyin + string
        else:
            result = string + pinyin
        return result
    else:
        for pinyin in pinyin_list:
            if pinyin in string:
                result = string.replace(pinyin, '')
                return result
        return string

def upper_policy(string):
    count_0 = upper_dict.get(0, 0)
    count_1 = upper_dict.get(1, 0)
    if count_0 >= count_1:
        u_dict = structure_dict.get('U', {})
        if not u_dict:
            if string:
                char_to_uppercase = random.choice(string)
                return string.replace(char_to_uppercase, char_to_uppercase.upper(), 1)
        sorted_u = sorted(u_dict.items(), key=lambda x: x[1])
        for key, value in sorted_u:
            lowercase_letter = key.lower()
            if lowercase_letter in string:
                string = string.replace(lowercase_letter, key)
                return string
        if string:
            lowercase_chars = [char for char in string if char.islower()]
            if lowercase_chars:
                random_lower = random.choice(lowercase_chars)
                return string.replace(random_lower, random_lower.upper(), 1)
            else:
                first_key = sorted_u[0][0]
                position = random.choice(['prefix', 'suffix'])
                if position == 'prefix':
                    string = first_key + string
                else:
                    string = string + first_key
                return string
    elif count_1 > count_0:
        if not any(char.isupper() for char in string):
            return string
        else:
            return string.lower()

def symbol_policy(string):
    count_0 = symbol_dict.get(0, 0)
    count_1 = symbol_dict.get(1, 0)
    if count_0 >= count_1:
        symbol = random.choice(symbol_list)
        position = random.choice(['prefix', 'suffix'])
        if position == 'prefix':
            result = symbol + string
        else:
            result = string + symbol
        return result
    else:
        for symbol in symbol_list:
            if symbol in string:
                result = string.replace(symbol, '')
                return result
        return string

# Store the names of features and Gini index in a list
length_policy = [length_strucount_policy, length_name_policy, length_birthday_policy, length_pinyin_policy, length_upper_policy, length_symbol_policy]
gini_list = [
    ("length", gini_values["length"], length_policy),
    ("strucount", gini_values["strucount"], strucount_policy),
    ("name", gini_values["name"], name_policy),
    ("birthday", gini_values["birthday"], birthday_policy),
    ("pinyin", gini_values["pinyin"], pinyin_policy),
    ("upper", gini_values["upper"], upper_policy),
    ("symbol", gini_values["symbol"], symbol_policy)
]

gini_length = calculate_gini(length_count)
gini_strucount = calculate_gini(structure_count)
# gini_structure = calculate_gini(structure_dict)
gini_name = calculate_gini(name_dict)
gini_birthday = calculate_gini(birthday_dict)
gini_pinyin =calculate_gini(pinyin_dict)
gini_upper = calculate_gini(upper_dict)
gini_symbol = calculate_gini(symbol_dict)

def identify_length(data1, data2):
    # Determine whether the lengths of two strings are different
    if len(data1) != len(data2):
        return 1  # Length changes, return 1
    else:
        return 0  # The length has not changed, return 0

def identify_strucount(data1, data2):
    structure_types_1 = set()
    for char in data1:
        if char.islower():
            structure_types_1.add('lowercase')
        elif char.isupper():
            structure_types_1.add('uppercase')
        elif char.isdigit():
            structure_types_1.add('digit')
        else:
            structure_types_1.add('special')
    item_structure_1 = len(structure_types_1)
    structure_types_2 = set()
    for char in data2:
        if char.islower():
            structure_types_2.add('lowercase')
        elif char.isupper():
            structure_types_2.add('uppercase')
        elif char.isdigit():
            structure_types_2.add('digit')
        else:
            structure_types_2.add('special')
    item_structure_2 = len(structure_types_2)
    if item_structure_1 == item_structure_2:
        return 0
    else:
        return 1

def check_contains(string1, string2):
    if len(string1) > len(string2):
        string1, string2 = string2, string1  # Swap strings, ensuring that string1 is the shorter one.

    if string1 in string2:
        remaining_chars = string2.replace(string1, '')  # The remaining characters after removing string1
        return remaining_chars

def identify_name(data1, data2, name):
    result = check_contains(data1, data2)
    if result == None:
        return 0
    name_list = name_transform(name)
    for i, string in enumerate(name_list):
        if string in result:
            return 1
    return 0

def identify_birthday(data1, data2, birthday):
    result = check_contains(data1, data2)
    if result == None:
        return 0
    birthday_list = birthday_transform(birthday)
    for i, string in enumerate(birthday_list):
        if string in result:
            return 1
    return 0

def identify_pinyin(data1, data2, pinyin_list):
    result = check_contains(data1, data2)
    if result == None:
        return 0
    for i, string in enumerate(pinyin_list):
        if string in result:
            return 1
    return 0

def identify_upper(data2):
    for char in data2:
        if char.isupper():
            return 1
    return 0

def identify_symbol(data1, data2, symbol_list):
    result = check_contains(data1, data2)
    if result == None:
        return 0
    for i, string in enumerate(symbol_list):
        if string in result:
            return 1
    return 0

def gen_newpsw(sixth_data, attribute_list):
    if "length" in attribute_list:
        if "strucount" in attribute_list:
            sixth_data = length_strucount_policy(sixth_data)
        elif "name" in attribute_list:
            sixth_data = length_name_policy(name, sixth_data)
        elif "birthday" in attribute_list:
            sixth_data = length_birthday_policy(birthday, sixth_data)
        elif "pinyin" in attribute_list:
            sixth_data = length_pinyin_policy(sixth_data)
        elif "upper" in attribute_list:
            sixth_data = length_upper_policy(sixth_data)
        elif "symbol" in attribute_list:
            sixth_data = length_symbol_policy(sixth_data)
    else:
        # Handle cases where 'length' is not present
        for i in attribute_list:
            if i == "structure_count":
                sixth_data = strucount_policy(sixth_data)
            elif i == "name":
                sixth_data = name_policy(name, sixth_data)
            elif i == "birthday":
                sixth_data = birthday_policy(birthday, sixth_data)
            elif i == "pinyin":
                sixth_data = pinyin_policy(sixth_data)
            elif i == "upper":
                sixth_data = upper_policy(sixth_data)
            elif i == "symbol":
                sixth_data = symbol_policy(sixth_data)
    return sixth_data

def remove_sensitive_data(new_data, password):
    del_data = new_data
    for char in password:
        del_data = del_data.replace(char, "", 1)
    del_data_list = list(del_data)
    random.shuffle(del_data_list)
    del_num = len(new_data) - 12
    modified_del_data = ''.join(del_data_list[:-del_num])
    if random.choice([True, False]):
        return modified_del_data + password
    else:
        return password + modified_del_data


data_list = []
with open("__file__", 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        path = line.split('--')
        sixth_data = path[5]
        seventh_data = path[6].replace('\n', '')
        password = seventh_data
        name = path[1]
        id = path[2]
        birthday = id[6:14]
        attribute_list = []
        length_change = identify_length(seventh_data, sixth_data)
        strucount_change = identify_strucount(seventh_data, sixth_data)
        name_change = identify_name(seventh_data, sixth_data, name)
        birthday_change = identify_birthday(seventh_data, sixth_data, birthday)
        pinyin_change = identify_pinyin(seventh_data, sixth_data, pinyin_list)
        upper_change = identify_upper(sixth_data)
        symbol_change = identify_symbol(seventh_data, sixth_data, symbol_list)
        if length_change == 1:
            gini_list = [(attr, gini, policy) for attr, gini, policy in gini_list if attr != "length"]
        if strucount_change == 1:
            gini_list = [(attr, gini, policy) for attr, gini, policy in gini_list if attr != "strucount"]
        if name_change == 1:
            gini_list = [(attr, gini, policy) for attr, gini, policy in gini_list if attr != "name"]
        if birthday_change == 1:
            gini_list = [(attr, gini, policy) for attr, gini, policy in gini_list if attr != "birthday"]
        if pinyin_change == 1:
            gini_list = [(attr, gini, policy) for attr, gini, policy in gini_list if attr != "pinyin"]
        if upper_change == 1:
            gini_list = [(attr, gini, policy) for attr, gini, policy in gini_list if attr != "upper"]
        if symbol_change == 1:
            gini_list = [(attr, gini, policy) for attr, gini, policy in gini_list if attr != "symbol"]
        gini_list.sort(key=lambda x: x[1], reverse=False)  # Sort in ascending order based on Gini index
        for item in gini_list[:2]:
            first_value = item[0]
            attribute_list.append(first_value)
        found = False
        iteration = 0
        while not found and iteration < 100:
            new_data = gen_newpsw(seventh_data, attribute_list)
            if len(new_data) < 13:
                found = True
                new_password = new_data
            else:
                iteration += 1
        if len(new_data) >= 13:
            new_password = remove_sensitive_data(new_data, password)
        print(name + "--" + password + "--" + new_password)
        data_list.append(new_password)
        length_count = length_extraction(new_password, length_count)
        structure_count = strucount_extraction(new_password, structure_count)
        structure_dict = structure_extraction(new_password, structure_dict)
        name_dict = name_extraction(new_password, name, name_dict)
        birthday_dict = birthday_extraction(new_password, birthday, birthday_dict)
        pinyin_dict = pinyin_extraction(new_password, pinyin_list, pinyin_dict)
        upper_dict = uppercase_extraction(new_password, upper_dict)
        symbol_dict = symbol_extraction(new_password, symbol_dict)
        gini_values = {
            "length": calculate_gini(length_count),
            "strucount": calculate_gini(structure_count),
            "name": calculate_gini(name_dict),
            "birthday": calculate_gini(birthday_dict),
            "pinyin": calculate_gini(pinyin_dict),
            "upper": calculate_gini(upper_dict),
            "symbol": calculate_gini(symbol_dict)
        }
        gini_list = [
            ("length", gini_values["length"], length_policy),
            ("strucount", gini_values["strucount"], strucount_policy),
            ("name", gini_values["name"], name_policy),
            ("birthday", gini_values["birthday"], birthday_policy),
            ("pinyin", gini_values["pinyin"], pinyin_policy),
            ("upper", gini_values["upper"], upper_policy),
            ("symbol", gini_values["symbol"], symbol_policy)
        ]
    print(data_list)
    with open("__newfile__", 'w', encoding="utf-8") as file:
        for item in data_list:
            file.write(str(item) + '\n')

