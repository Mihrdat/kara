from rest_framework.viewsets import ModelViewSet
from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
