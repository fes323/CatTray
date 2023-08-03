from django.urls import include, path
from wallet import views


urlpatterns = [
    path('wallet/', views.wallet, name='wallet')
]