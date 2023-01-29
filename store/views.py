from django.db.models import Count

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
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
from .permissions import IsAdminOrReadOnly
from .pagination import DefaultPagination

from user.models import Customer


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).exists():
            return Response({'detail': 'Collection cannot be deleted, because it includes one or more products.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product')
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    def get_queryset(self):
        return CartItem.objects \
                       .filter(cart_id=self.kwargs['cart_pk']) \
                       .select_related('product')

    def get_serializer_class(self):
        if self.action == 'create':
            return CartItemCreateSerializer
        elif self.request.method in ['update', 'partial_update']:
            return CartItemUpdateSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


class OrderViewSet(CreateModelMixin,
                   ListModelMixin,
                   RetrieveModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=Customer.objects.get(user=user))

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(
            data=request.data, context={'user': self.request.user})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
