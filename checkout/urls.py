from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<payment_reference>',views.checkout_success, name='checkout_success'),
    path('cache_checkout_data/',views.cache_checkout_data,name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),
    path('cancel_membership/<str:payment_reference>/', views.cancel_membership, name='cancel_membership'),

]