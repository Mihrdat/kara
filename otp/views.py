from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login, get_user_model
from .serializers import CreateOTPSerializer, VerifyOTPSerializer

User = get_user_model()


@api_view(['POST'])
def create_otp(request):
    if request.method == 'POST':
        serializer = CreateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def verify_otp(request):
    if request.method == 'POST':
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        user = User.objects.get(pk=user_id)
        login(request, user)

        return Response({'detail': 'You have successfully logged in.'})
