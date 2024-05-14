from django.urls import path
from app import views

urlpatterns = [
    path(route='', view=views.principal, name='principal'),
    path(route='file_upload/', view=views.file_upload, name='file_upload'),
]
