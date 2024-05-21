from django.urls import path
from . import views

urlpatterns = [
    path('', views.plans, name='plans'),
    path('add/', views.add_plan, name='add_plan'),
    path('edit/<int:plan_id>/', views.edit_plan, name='edit_plan'),
    path('delete/<int:plan_id>/', views.delete_plan, name='delete_plan'),
]