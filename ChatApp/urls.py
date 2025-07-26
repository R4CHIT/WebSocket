from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', room, name='home'),
    path('message/<str:username>/<str:room_name>', message, name='room'),
]
