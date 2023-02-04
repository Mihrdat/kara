from django.db.models import Count

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)

from .models import (
    Collection,
    Product,
    Cart,
    CartItem,
    Order,
)
from .serializers import (
    CollectionSerializer,
    ProductSerializer,
    CartSerializer,
    CartItemCreateSerializer,
    CartItemUpdateSerializer,
    CartItemSerializer,
    OrderCreateSerializer,
    OrderSerializer,
)
from .throtteling import CartAnonRateThrottle, CartUserRateThrottle

from user.models import Customer


class CollectionViewSet(ListModelMixin, GenericViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer


class ProductViewSet(ListModelMixin,
                     RetrieveModelMixin,
                     GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product')
    serializer_class = CartSerializer
    throttle_classes = [CartAnonRateThrottle, CartUserRateThrottle]


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.select_related('product')

    def get_queryset(self):
        return self.queryset \
                   .filter(cart_id=self.kwargs['cart_pk']) \
                   .select_related('product')

    def get_serializer_class(self):
        if self.action == 'create':
            return CartItemCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CartItemUpdateSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


class OrderViewSet(CreateModelMixin,
                   ListModelMixin,
                   RetrieveModelMixin,
                   GenericViewSet):
    queryset = Order.objects \
                    .select_related('customer__user') \
                    .prefetch_related('items__product')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return self.queryset.filter(customer=customer)

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
