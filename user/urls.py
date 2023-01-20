from django.urls import path
from . import views


urlpatterns = [
    path('otp/create/', views.create),
    path('otp/verify/', views.verify),
]
