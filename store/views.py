from django.db.models import Count

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
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
from .throttling import CartAnonRateThrottle, CartUserRateThrottle

from user.models import Customer


class CollectionViewSet(ListModelMixin, GenericViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product')
    serializer_class = CartSerializer
    throttle_classes = [CartAnonRateThrottle, CartUserRateThrottle]

    def create(self, request, *args, **kwargs):
        if request.COOKIES.get('cart_id'):
            return Response({'detail': 'There is currently a shopping cart.'}, status=status.HTTP_409_CONFLICT)
        response = super().create(request, *args, **kwargs)
        response.set_cookie(key='cart_id', value=response.data['id'])
        return response

    @action(detail=False, permission_classes=[IsAuthenticated])
    def mine(self, request):
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)

        cookie_cart_id = request.COOKIES.get('cart_id')
        if cookie_cart_id != str(cart.id):
            cart_items = CartItem.objects \
                                 .filter(cart_id=cookie_cart_id) \

            for item in cart_items:
                CartItem.objects.update_or_create(
                    product_id=item.product_id,
                    cart_id=cart.id,
                    defaults={'quantity': item.quantity}
                )

            Cart.objects.filter(pk=cookie_cart_id).delete()

        serializer = self.get_serializer(cart)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        response.set_cookie(key='cart_id', value=cart.id)
        return response


class CartItemViewSet(ModelViewSet):
    def get_queryset(self):
        return CartItem.objects \
                       .select_related('product') \
                       .filter(cart_id=self.kwargs['cart_pk']) \
                       .select_related('product')

    def get_serializer_class(self):
        if self.action == 'create':
            return CartItemCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CartItemUpdateSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['cart_id'] = self.kwargs['cart_pk']
        return context


class OrderViewSet(CreateModelMixin,
                   ListModelMixin,
                   RetrieveModelMixin,
                   GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return Order.objects \
                    .filter(customer=customer) \
                    .select_related('customer__user') \
                    .prefetch_related('items__product')

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
