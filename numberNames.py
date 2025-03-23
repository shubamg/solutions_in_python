ZERO = 'zero'
digit_names = [ZERO, 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
tens_place_names = [None, None, 'twen', 'thir', 'for', 'fif', 'six', 'seven', 'eigh', 'nine']
triplet_levels = ['', 'thousand', 'million', 'billion', 'trillion']
HUNDRED = 'hundred'
THOUSAND_NUM = 1000
AND = 'and'
TENS_SUFFIX = 'ty'
ten_to_nineteen = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen',
        'eighteen', 'nineteen']
AND = 'and'
COMMA = ','


def get_reverse_name_of_three_digit_number(num):
    name = []
    hundred_digit = num // 100
    if hundred_digit > 0:
        name.extend([digit_names[hundred_digit], HUNDRED])
    tens_digit = (num // 10) % 10
    units_digit = num % 10
    if USE_AND and hundred_digit and (tens_digit or units_digit):
        name.append(AND)
    if tens_digit == 1:
        name.append(ten_to_nineteen[units_digit])
    else:
        if tens_digit > 1:
            name.append(tens_place_names[tens_digit] + TENS_SUFFIX)
        if units_digit > 0:
            name.append(digit_names[units_digit])
    name.reverse()
    return name


def get_number_name(number):
    original_number = number
    reverse_number_name_list = []
    three_digit_block_index = 0
    insert_comma = False
    while number > 0:
        if three_digit_block_index == len(triplet_levels):
            raise Exception('Oops!! Cannot handle such a large number yet!!')
        three_digits = number % THOUSAND_NUM
        three_digits_name = get_reverse_name_of_three_digit_number(three_digits)
        three_digits_name = [word for word in three_digits_name if word != '']
        if len(three_digits_name):
            reverse_number_name_list.append(triplet_levels[three_digit_block_index])
            if insert_comma and USE_COMMA:
                reverse_number_name_list[-1] += COMMA
            reverse_number_name_list.extend(three_digits_name)
            insert_comma = True
        three_digit_block_index += 1
        number //= THOUSAND_NUM
    reverse_number_name_list.reverse()
    if not len(reverse_number_name_list):
        reverse_number_name_list.append(ZERO)
    number_name = ' '.join(reverse_number_name_list)
    if CAPITALIZE_NAME:
        number_name = number_name.capitalize()
    return original_number, number_name


def print_number_names(input_numbers):
    tuples = (get_number_name(number) for number in input_numbers)
    for number, name in tuples:
        print('{0}: {1}'.format(number, name))


USE_AND = True
USE_COMMA = True
CAPITALIZE_NAME = True
input_numbers = [0, 123, 123456, 123000000000000000]
print_number_names(input_numbers)
