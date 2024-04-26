from django.urls import path
from . import views

urlpatterns = [
    path('', views.trainer_list, name='trainers'),
    path('<int:trainer_id>/', views.trainer_detail, name='trainer_detail'),
]