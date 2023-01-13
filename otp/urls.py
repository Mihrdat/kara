from django.urls import path
from . import views


urlpatterns = [
    path('otp/create/', views.CreateOTP.as_view()),
    path('otp/verify/', views.VerifyOTP.as_view()),
]
