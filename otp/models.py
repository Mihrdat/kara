import random
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .validators import validate_phone_number_format

NUMBER_OF_DIGITS = 6


def generate_random_code():
    choices = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    return ''.join(random.choices(choices, k=NUMBER_OF_DIGITS))


def set_expiration_time():
    return timezone.now() + timedelta(minutes=5)


class OTP(models.Model):
    expiration_time = models.DateTimeField(default=set_expiration_time)
    phone_number = models.CharField(
        max_length=11, validators=[validate_phone_number_format])
    code = models.CharField(
        max_length=NUMBER_OF_DIGITS, default=generate_random_code)
