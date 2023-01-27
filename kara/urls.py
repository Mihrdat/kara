from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from user import views as user_views
from store import views as store_views

admin.site.site_header = 'Kara Administration'

router = routers.DefaultRouter()
router.register('customers', user_views.CustomerViewSet)
router.register('collections', store_views.CollectionViewSet)
router.register('products', store_views.ProductViewSet)
router.register('carts', store_views.CartViewSet)

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register(
    'items', store_views.CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(carts_router.urls)),
]
