from otp.models import OTP
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=OTP)
def send_code_of_new_OTP_to_client(sender, **kwargs):
    if kwargs['created']:
        otp = kwargs['instance']
        print(f'{otp.code} was sent to {otp.user.phone_number} using Twilio.')
