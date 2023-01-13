import re
from django.core.exceptions import ValidationError


def validate_phone_number_format(phone_number):
    ir_mobile_regex = '^(0|0098|\+98)9(0[1-5]|[1 3]\d|2[0-2]|98)\d{7}$'

    if not bool(re.search(ir_mobile_regex, phone_number)):
        raise ValidationError('Please enter a valid phone number.')
