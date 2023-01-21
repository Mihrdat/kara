from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import serializers
from .utils import is_valid_phone_number

User = get_user_model()


class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, phone_number):
        if not is_valid_phone_number(phone_number):
            raise serializers.ValidationError('Please enter a valid number.')

        if cache.get(key=phone_number):
            raise serializers.ValidationError(
                'You have just sent a request. If you have not received the code, please wait until you can send another request.')

        return phone_number


class VerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs['phone_number']
        code = attrs['code']
        value = cache.get(key=phone_number)

        if value is None:
            raise serializers.ValidationError(
                'First, request to send an OTP code to this phone number.')
        elif value != code:
            raise serializers.ValidationError('The given code is invalid.')

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number']
