from django.urls import include, path
from main import views


urlpatterns = [
    path('', views.main_page, name='main_page')
]