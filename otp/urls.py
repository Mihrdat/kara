from django.urls import path
from . import views


urlpatterns = [
    path('otp/create/', views.create_otp),
    path('otp/verify/', views.verify_otp),
]
