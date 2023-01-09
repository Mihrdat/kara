from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import OTP

User = get_user_model()


class CreateOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True)
    user_id = serializers.IntegerField(read_only=True)

    def validate_phone_number(self, phone_number):
        if not User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                'No user with the given phone number was found.')
        return phone_number

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        user = User.objects.get(phone_number=phone_number)
        return OTP.objects.create(user=user)


class VerifyOTPSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField()

    def validate(self, attrs):
        code = attrs['code']
        user_id = attrs['user_id']
        otp = OTP.objects.get_or_none(code=code, user_id=user_id)

        if otp is None or otp.is_expired():
            raise serializers.ValidationError('Invalid OTP code.')

        return attrs
