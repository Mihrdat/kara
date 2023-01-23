from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, get_user_model
from django.core.cache import cache
from store.models import Customer
from .serializers import SendOTPSerializer, VerifySerializer, CustomerSerializer
from .utils import generate_random_code

User = get_user_model()


class CustomerViewSet(GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def send_otp(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        if cache.get(key=phone_number):
            return Response({'detail': 'You have just sent a request. If you have not received the code, please wait until you can send another request.'})

        code = generate_random_code(number_of_digits=6)
        cache.set(key=phone_number, value=code, timeout=2 * 60)
        print(code)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def verify(self, request):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        user, created = User.objects.get_or_create(phone_number=phone_number)
        customer, created = Customer.objects.get_or_create(user=user)
        login(request, user)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
