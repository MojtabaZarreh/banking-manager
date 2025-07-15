# transactions/urls.py
from django.urls import path
from .views import submit, transaction_list_api

urlpatterns = [
    path('submit-transaction/', submit, name='submit_transaction'),
    
    path('api/history/', transaction_list_api, name='transaction-list-api'),
]