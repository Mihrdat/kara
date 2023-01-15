import random
from django.db import models
from django.utils import timezone
from datetime import timedelta

NUMBER_OF_DIGITS = 6


def generate_random_code():
    choices = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    return ''.join(random.choices(choices, k=NUMBER_OF_DIGITS))


def set_expiration_time():
    return timezone.now() + timedelta(minutes=5)
