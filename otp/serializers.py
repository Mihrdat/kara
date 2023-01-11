from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import OTP

User = get_user_model()


class CreateOTPSerializer(serializers.ModelSerializer):
    expiration_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = OTP
        fields = ['phone_number', 'expiration_time']

    def validate_phone_number(self, phone_number):
        if not User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                'No user with the given phone number was found.')
        return phone_number

    def validate(self, attrs):
        phone_number = attrs['phone_number']
        current_time = timezone.now()

        if OTP.objects \
              .filter(phone_number=phone_number, expiration_time__gt=current_time) \
              .exists():
            raise serializers.ValidationError(
                {'detail': 'We have just sent you a valid code. Please wait until you can make another request.'})

        return attrs


class VerifyOTPSerializer(serializers.Serializer):
    code = serializers.CharField()
    phone_number = serializers.CharField()

    def validate(self, attrs):
        code = attrs['code']
        phone_number = attrs['phone_number']
        current_time = timezone.now()

        if OTP.objects \
              .filter(code=code, phone_number=phone_number, expiration_time__gt=current_time) \
              .first() is None:
            raise serializers.ValidationError('The given OTP code is invalid.')

        return attrs
