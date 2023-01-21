from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import login, get_user_model
from django.core.cache import cache
from .serializers import CreateOTPSerializer, VerifySerializer, UserSerializer
from .utils import generate_random_code

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


@api_view(['POST'])
def create(request):
    serializer = CreateOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone_number = serializer.validated_data['phone_number']

    if cache.get(key=phone_number):
        return Response({'detail': 'You have just sent a request. If you have not received the code, please wait until you can send another request.'})

    code = generate_random_code(number_of_digits=6)
    cache.set(key=phone_number, value=code, timeout=(2 * 60))
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def verify(request):
    serializer = VerifySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone_number = serializer.validated_data['phone_number']
    code = serializer.validated_data['code']
    value = cache.get(key=phone_number)

    if value != code:
        return Response({'detail': 'The given code is invalid.'})

    (user, is_created) = User.objects.get_or_create(phone_number=phone_number)
    login(request, user)
    return Response({'user_id': user.id}, status=status.HTTP_200_OK)
