from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<reference>', views.checkout_success, name='checkout_success'),
    path('checkout/error/', views.checkout_error, name='checkout_error'),
]