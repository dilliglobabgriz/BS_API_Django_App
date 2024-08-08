from django.urls import path
from . import views

urlpatterns = [
    path('player_info/', views.player_info, name='player_info'),
]