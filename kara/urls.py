from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Kara Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
]
