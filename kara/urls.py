from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from user import views as user_views
from store import views as store_views

admin.site.site_header = "Kara Administration"

router = DefaultRouter()
router.register("customers", user_views.CustomerViewSet)
router.register("collections", store_views.CollectionViewSet)
router.register("products", store_views.ProductViewSet)
router.register("carts", store_views.CartViewSet)
router.register(
    "carts/(?P<cart_pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/items",
    store_views.CartItemViewSet,
    basename="cart-items",
)
router.register("orders", store_views.OrderViewSet, basename="orders")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/v1/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
