from django.urls import path
from . import views

urlpatterns = [
    path('', views.trainer_list, name='trainers'),
    path('<int:trainer_id>/', views.trainer_detail, name='trainer_detail'),
    path('add/', views.add_trainer, name='add_trainer'),
    path('edit/<int:trainer_id>/', views.edit_trainer, name='edit_trainer'),
    path('delete/<int:trainer_id>/', views.delete_trainer, name='delete_trainer'),
]