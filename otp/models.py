from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random

NUMBER_OF_DIGITS = 6


def generate_random_code():
    choices = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    return ''.join(random.choices(choices, k=NUMBER_OF_DIGITS))


def set_expiration_time():
    # The expiration time is 5 minutes after creation.
    return timezone.now() + timedelta(minutes=5)


class OTPManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return OTP.objects.get(**kwargs)
        except OTP.DoesNotExist:
            return None


class OTP(models.Model):
    objects = OTPManager()
    expiration_time = models.DateTimeField(default=set_expiration_time)
    code = models.CharField(
        max_length=NUMBER_OF_DIGITS, default=generate_random_code)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def is_expired(self):
        return not timezone.now() < self.expiration_time
