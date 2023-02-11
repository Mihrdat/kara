from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from .choices import OrderStatus
from uuid import uuid4
from user.models import Customer


class Collection(models.Model):
    name = models.CharField(max_length=55, unique=True)
    parent_collection = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ProductImage(models.Model):
    image = models.ImageField(upload_to='store/images')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateField(auto_now_add=True)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, null=True, blank=True)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')

    class Meta:
        unique_together = [['cart', 'product']]


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    status = models.IntegerField(
        choices=OrderStatus.CHOICES, default=OrderStatus.PENDING)


class OrderItem(models.Model):
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='items')


class OrderStatusLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    previous_status = models.IntegerField(
        choices=OrderStatus.CHOICES, default=0)
    current_status = models.IntegerField(
        choices=OrderStatus.CHOICES, default=OrderStatus.PENDING)
    performer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='status_logs')
