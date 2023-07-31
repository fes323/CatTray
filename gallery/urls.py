from django.urls import include, path
from gallery import views


urlpatterns = [
    path('gallery', views.gallery, name='gallery')
]