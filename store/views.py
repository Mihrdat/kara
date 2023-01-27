from django.db.models import Count

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)

from .models import (
    Collection,
    Product,
    Cart,
    CartItem,
)
from .serializers import (
    CollectionSerializer,
    ProductSerializer,
    CartSerializer,
    CartItemCreateSerializer,
    CartItemUpdateSerializer,
    CartItemSerializer
)
from .permissions import IsAdminOrReadOnly
from .pagination import DefaultPagination


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
    # We do not allow PUT request.
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        return CartItem.objects \
                       .filter(cart_id=self.kwargs['cart_pk']) \
                       .select_related('product')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartItemCreateSerializer
        elif self.request.method == 'PATCH':
            return CartItemUpdateSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
