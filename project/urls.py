from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),

    path('create/', views.create, name='create_project'), 
    # path('create/success/', views.success, name='success'), # Not needed

    path('update/<int:project_id>', views.update, name='update_project'),

    path('project/<int:project_id>/', views.get, name='retrieve_project',),
    path('project/', views.get_all, name='retrieve_all_project'),

    path('delete/<int:project_id>/', views.delete, name='delete_project'), # I made a URL to respect instructions
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 