from django.urls import path
from app import views

urlpatterns = [
    path(route='', view=views.principal, name='principal'),
    path(route='upload/', view=views.upload, name='upload'),
    path(route='upload_csv/', view=views.upload_csv, name='upload_csv'),
]
