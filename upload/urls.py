from django.urls import include, path

urlpatterns = [
    path(route='', view=include(arg='app.urls')),
]
