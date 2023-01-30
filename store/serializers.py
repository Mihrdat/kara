from rest_framework import serializers
from django.db import transaction
from .models import (
    Collection,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
)
from user.models import Customer
from user.serializers import CustomerSerializer


class CollectionSerializer(serializers.ModelSerializer):
    parent_collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(), allow_null=True)
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'products_count', 'parent_collection']


class ProductSerializer(serializers.ModelSerializer):
    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all())

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'unit_price',
            'collection',
        ]


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartItemCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    def create(self, validated_data):
        cart_id = self.context['cart_id']
        product_id = validated_data['product_id']
        quantity = validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'quantity',
            'unit_price',
        ]


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'created_at',
            'customer',
            'items',
        ]


class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_cart_id(self, cart_id):
        try:
            cart = Cart.objects.get(id=cart_id)
            if cart.items.count() == 0:
                raise serializers.ValidationError('The cart is empty.')
        except Cart.DoesNotExist:
            raise serializers.ValidationError(
                'No cart with the given ID was found.')

        return cart_id

    @transaction.atomic()
    def create(self, validated_data):
        cart_id = validated_data['cart_id']
        user = validated_data['user']
        customer = Customer.objects.get(user=user)
        order = Order.objects.create(customer=customer)

        cart_items = CartItem.objects \
                             .filter(cart_id=cart_id) \
                             .select_related('product')

        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.unit_price
            ) for item in cart_items
        ]

        OrderItem.objects.bulk_create(order_items)
        Cart.objects.filter(pk=cart_id).delete()

        return order
