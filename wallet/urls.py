from django.urls import include, path
from wallet import views
from wallet.api_views import TransactionCategoryListApiView


urlpatterns = [
    path('transaction_category/create/', views.manage_transaction_category, name='transaction_category_create'),
    path('transaction_category/update/<str:pk>/', views.manage_transaction_category, name='transaction_category_update'),
    path('wallet/', views.wallet, name='wallet'),
    path('detail_wallets/', views.detail_wallets, name='detail_wallets'),
    path('manage_wallet/<uuid:wallet_uuid>/', views.manage_wallet, name='manage_wallet'),
    path('manage_wallet/', views.manage_wallet, name='manage_wallet'),
    path('delete_wallet/<uuid:wallet_uuid>/', views.delete_wallet, name='delete_wallet'),
    
    path('api/transaction_categories/', TransactionCategoryListApiView.as_view(), name='api_transaction_category_list'),
]