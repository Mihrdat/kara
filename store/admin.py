from django.contrib import admin, messages
from django.urls import reverse, path
from django.shortcuts import redirect
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from .models import Collection, Product, Order
from .choices import OrderStatus


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
    list_display = ['created_at', 'customer', 'status', 'change_status']
    list_per_page = 15
    list_editable = ['status']
    list_select_related = ['customer__user']

    def get_urls(self):
        custom_urls = [
            path('do_change_status/<int:order_id>/',
                 self.do_change_status,
                 name='do_change_status'
                 ),
        ]
        return custom_urls + super().get_urls()

    def change_status(self, order):
        url = reverse('admin:do_change_status', args=[order.id])
        button = 'Change' if order.status == OrderStatus.NEW else ''
        return format_html('<a href="{}">{}</a>', url, button)

    def do_change_status(self, request, order_id):
        order = Order.objects.get(id=order_id)
        order.status = OrderStatus.PROCESSING
        order.save(update_fields=['status'])
        self.message_user(request, 'Status were successfully updated.')
        return redirect('admin:store_order_changelist')
