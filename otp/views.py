from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login, get_user_model
from .serializers import CreateOTPSerializer, VerifyOTPSerializer

User = get_user_model()


@api_view(['POST'])
def create(request):
    serializer = CreateOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def verify(request):
    serializer = VerifyOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    phone_number = serializer.validated_data['phone_number']
    (user, is_created) = User.objects.get_or_create(phone_number=phone_number)

    login(request, user)
    return Response({'detail': 'You have successfully logged in.'}, status=status.HTTP_200_OK)
