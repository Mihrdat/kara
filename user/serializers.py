from rest_framework import serializers
from django.core.cache import cache
from django.contrib.auth import get_user_model
from store.models import Customer
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
        if value != code:
            raise serializers.ValidationError('The given code is invalid.')

        return attrs


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number']


class CustomerSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'birth_date', 'user']
