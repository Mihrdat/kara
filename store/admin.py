from django.contrib import admin
from django.urls import reverse
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from .models import Collection, Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'unit_price', 'collection']
    list_editable = ['unit_price']
    list_filter = ['collection', 'created_at']
    list_per_page = 15
    search_fields = ['name']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({'collection__id': str(collection.id)})
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('products'))


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'customer', 'status']
    list_per_page = 15
    list_editable = ['status']
    list_select_related = ['customer__user']
