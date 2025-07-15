from django.urls import path
from .views import master

urlpatterns = [
    path('', master, name='master')
]