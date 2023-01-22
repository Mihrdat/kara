from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views

admin.site.site_header = 'Kara Administration'

router = DefaultRouter()
router.register('customers', views.CustomerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
