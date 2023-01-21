from django.db import models
from user.models import Customer
from django.core.validators import MinValueValidator
from uuid import uuid4


class Collection(models.Model):
    name = models.CharField(max_length=55, unique=True)

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


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateField(auto_now_add=True)


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


class OrderItem(models.Model):
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='items')
