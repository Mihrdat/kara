from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=55, unique=True)


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    last_update = models.DateField(auto_now=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products')
