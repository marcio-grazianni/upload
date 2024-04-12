from django.urls import path
from django.urls.resolvers import URLPattern
from app import views


urlpatterns: list[URLPattern] = [
    path(route='upload/', view=views.file_upload, name='file_upload'),
]
