
from django.urls import path
from .views import monthly_summary_view, monthly_suggestions_view, ocr_transaction_view

urlpatterns = [
    path('api/summary/', monthly_summary_view, name='monthly-summary'),
    path('api/analytics/', monthly_suggestions_view, name='monthly-suggestions'),
    path('api/photo/', ocr_transaction_view, name='ocr-transaction'),
]
