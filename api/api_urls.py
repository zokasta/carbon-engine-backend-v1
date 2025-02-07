from django.urls import path
from .views.apiCreate import api_generator
from .views.create import create_api
from .views.delete import delete_api
from .views.updateDatabase import update_database_name

urlpatterns = [
    path('generate-api/', api_generator, name='generate_api'),
    path('create-api/', create_api, name='create_api'),
    path('delete-api/', delete_api, name='delete_api'),
    path('update-database/', update_database_name, name='for-update-database'),
]
