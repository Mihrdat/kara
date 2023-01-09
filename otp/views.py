from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CreateOTPSerializer


@api_view(['POST'])
def create_otp(request):
    if request.method == 'POST':
        serializer = CreateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
