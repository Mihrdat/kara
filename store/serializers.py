from rest_framework import serializers
from .models import Collection, Product, Cart


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'products_count']


class ProductSerializer(serializers.ModelSerializer):
    collection_id = serializers.IntegerField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'unit_price',
            'collection_id',
        ]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'created_at',
        ]
