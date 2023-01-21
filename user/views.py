from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from django.contrib.auth import login, get_user_model
from django.core.cache import cache
from store.models import Customer
from .serializers import SendOTPSerializer, VerifySerializer, UserSerializer
from .utils import generate_random_code

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def send_otp(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        code = generate_random_code(number_of_digits=6)
        cache.set(key=phone_number, value=code, timeout=2 * 60)
        print(code)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def verify(self, request):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        (user, is_created) = User.objects.get_or_create(phone_number=phone_number)
        if is_created:
            Customer.objects.create(user=user)

        login(request, user)
        return Response({'user_id': user.id}, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'send_otp':
            return SendOTPSerializer
        if self.action == 'verify':
            return VerifySerializer
        return UserSerializer
