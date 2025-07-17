
from django.urls import path
from .views import monthly_summary_view

urlpatterns = [
    path('api/summary/', monthly_summary_view, name='monthly-summary'),
]
