from django.urls import include, path
from blog import views


urlpatterns = [
    path('blog', views.blog_list, name='blog_list')
]