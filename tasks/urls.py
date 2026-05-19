from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('tasks/', views.task_list),
    path('create/', views.task_create),
    path('edit/<int:pk>/', views.task_edit),
    path('delete/<int:pk>/', views.task_delete),
    path('register/', views.register_view),
]