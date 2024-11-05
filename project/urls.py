from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='create_project'),
    path('update/<int:projet_id>', views.update, name='update_project'),
    path('get/<int:project_id>/', views.get, name='retrieve_project'),
    path('get/', views.get_all, name='retrieve_project'),
    path('delete/<int:project_id>/', views.delete, name='delete_project'),
]