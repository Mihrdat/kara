from django.contrib import admin
from django.shortcuts import render
from django.urls import reverse, path
from django.shortcuts import redirect
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from .models import Collection, Product, Order, InventoryMovement
from .choices import OrderStatus


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "reason",
        "type",
        "display_quantity",
    ]

    def display_quantity(self, inventory_movement):
        if inventory_movement.reason in inventory_movement.INCREMENTAL_REASONS:
            return "+" + str(inventory_movement.quantity)
        else:
            return "-" + str(inventory_movement.quantity)

    display_quantity.short_description = "quantity"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "unit_price", "collection", "inventory"]
    list_editable = ["unit_price"]
    list_filter = ["collection", "created_at"]
    list_per_page = 15
    search_fields = ["name"]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["name", "products_count"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("products"))


class FilterByID(admin.SimpleListFilter):
    title = "id"
    parameter_name = "id"
    template = "filter_by_id.html"

    def lookups(self, request, model_admin):
        value = request.GET.get("id")
        return [(value, "input")]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(pk=self.value())
        return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "created_at",
        "customer",
        "status",
        "paid_button",
        "total_price",
    ]
    list_per_page = 15
    list_select_related = ["customer__user"]
    list_filter = ["status", FilterByID]

    def get_urls(self):
        custom_urls = [
            path(
                "<int:order_id>/confirm_paid/",
                self.confirm_view,
                name="store_order_confirm_paid",
            ),
            path("<int:order_id>/paid/", self.paid_view, name="store_order_paid"),
        ]
        return custom_urls + super().get_urls()

    def total_price(self, order):
        return sum(
            [item.quantity * item.product.unit_price for item in order.items.all()]
        )

    def paid_button(self, order):
        url = reverse("admin:store_order_confirm_paid", args=[order.id])
        if order.status == OrderStatus.NEW:
            return format_html('<a href="{}">{}</a>', url, "Change")

    def confirm_view(self, request, order_id):
        order = self.get_object(request, order_id)
        context = {
            **self.admin_site.each_context(request),
            "opts": Order._meta,
            "order": order,
            "original": order,
        }
        return render(request, "confirm_paid.html", context)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("items__product")

    def paid_view(self, request, order_id):
        order = self.get_object(request, order_id)
        order.change_status(new_status=OrderStatus.PROCESSING, user=request.user)
        self.message_user(request, "Status were successfully updated.")
        return redirect("admin:store_order_changelist")
