from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, get_user_model
from .serializers import CreateOTPSerializer

User = get_user_model()


class CreateOTP(APIView):
    def post(self, request):
        serializer = CreateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# def verify_otp(request):
#     if request.method == 'POST':
#         serializer = VerifyOTPSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user_id = serializer.validated_data['user_id']
#         user = User.objects.get(pk=user_id)
#         login(request, user)

#         return Response({'detail': 'You have successfully logged in.'})
