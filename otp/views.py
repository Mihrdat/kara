from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login, get_user_model
from django.core.cache import cache
from .serializers import CreateOTPSerializer, VerifyOTPSerializer
from .utils import generate_random_code


User = get_user_model()


@api_view(['POST'])
def create(request):
    serializer = CreateOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    phone_number = serializer.data['phone_number']
    code = generate_random_code(number_of_digits=6)
    cache.set(key=phone_number, value=code)

    print(code)  # Send code to the client using Twilio.
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def verify(request):
    serializer = VerifyOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    phone_number = serializer.data['phone_number']
    code = serializer.data['code']
    value = cache.get(key=phone_number)

    if value is None or value != code:
        return Response({'detail': 'The given code is invalid.'})
    else:
        (user, is_created) = User.objects.get_or_create(phone_number=phone_number)
        login(request, user)
        return Response({'detail': 'You have successfully logged in.'}, status=status.HTTP_200_OK)
