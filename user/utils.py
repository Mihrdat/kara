import re
import random


def is_valid_phone_number(phone_number):
    ir_mobile_regex = '^(0|0098|\+98)9(0[1-5]|[1 3]\d|2[0-2]|98)\d{7}$'
    return re.match(ir_mobile_regex, phone_number)


def generate_random_code(number_of_digits):
    choices = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    return ''.join(random.choices(choices, k=number_of_digits))
