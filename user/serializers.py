from rest_framework import serializers
from .utils import is_valid_phone_number


class CreateOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, phone_number):
        if not is_valid_phone_number(phone_number):
            raise serializers.ValidationError('Please enter a valid number.')
        return phone_number


class VerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()
