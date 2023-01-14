from django.utils import timezone
from rest_framework import serializers
from .models import OTP


class CreateOTPSerializer(serializers.ModelSerializer):
    expiration_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = OTP
        fields = ['phone_number', 'expiration_time']

    def create(self, validated_data):
        phone_number = validated_data['phone_number']

        if OTP.objects \
              .filter(phone_number=phone_number, expiration_time__gt=timezone.now()) \
              .exists():
            raise serializers.ValidationError(
                {'detail': 'We have just sent you a code. If you have not received it, please wait until you can send another request.'})

        return super().create(validated_data)


class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['code', 'phone_number']

    def validate(self, attrs):
        code = attrs['code']
        phone_number = attrs['phone_number']

        if OTP.objects \
              .filter(code=code, phone_number=phone_number, expiration_time__gt=timezone.now()) \
              .first() is None:
            raise serializers.ValidationError(
                {'detail': 'The given code is invalid.'})

        return attrs
