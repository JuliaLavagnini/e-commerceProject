from django.urls import path
from . import views


urlpatterns = [
    path('', views.profile, name='profile'),
    path('cancel_membership/<payment_reference>', views.cancel_membership, name='cancel_membership'),
    
]