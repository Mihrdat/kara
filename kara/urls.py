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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
