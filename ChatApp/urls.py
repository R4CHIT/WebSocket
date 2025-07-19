from django.contrib import admin
from django.urls import path
from .views import room

urlpatterns = [
    path('', room, name='home'),
]
