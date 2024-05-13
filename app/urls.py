from django.urls import path
from app import views

urlpatterns = [
    path(route='', view=views.file_upload, name='file_upload'),
]
