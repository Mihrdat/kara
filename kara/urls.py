from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views as user_views
from store import views as store_views

admin.site.site_header = 'Kara Administration'

router = DefaultRouter()
router.register('customers', user_views.CustomerViewSet)
router.register('collections', store_views.CollectionViewSet)
router.register('products', store_views.ProductViewSet)
router.register('carts', store_views.CartViewSet)
router.register('orders', store_views.OrderViewSet, basename='orders')

cart_items_list = store_views.CartItemViewSet.as_view(
    {'get': 'list', 'post': 'create'})
cart_items_detail = store_views.CartItemViewSet.as_view(
    {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/carts/<uuid:cart_pk>/items/', cart_items_list),
    path('api/v1/carts/<uuid:cart_pk>/items/<int:pk>/', cart_items_detail),
]
