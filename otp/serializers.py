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

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        current_time = timezone.now()

        if OTP.objects \
              .filter(phone_number=phone_number, expiration_time__gt=current_time) \
              .exists():
            raise serializers.ValidationError(
                'We have just sent you a valid code. Please wait until you can make another request.')

        return super().create(validated_data)


# class VerifyOTPSerializer(serializers.Serializer):
#     user_id = serializers.IntegerField()
#     code = serializers.CharField()

#     def validate(self, attrs):
#         code = attrs['code']
#         user_id = attrs['user_id']
#         otp = OTP.objects.get_or_none(code=code, user_id=user_id)

#         if otp is None or otp.is_expired():
#             raise serializers.ValidationError('Invalid OTP code.')

#         return attrs
