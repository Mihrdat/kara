from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, get_user_model
from .serializers import CreateOTPSerializer, VerifyOTPSerializer

User = get_user_model()


class CreateOTP(APIView):
    def post(self, request):
        serializer = CreateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyOTP(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        user = User.objects.get(phone_number=phone_number)
        login(request, user)

        return Response({'detail': 'You have successfully logged in.'})
