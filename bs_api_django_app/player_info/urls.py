from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('player_info/', views.player_info, name='player_info'),
    path('player_info/details/<int:id>', views.details, name='details'),
    path('top_global/details_general/<str:id>', views.details_general, name='details_general'),
    path('top_global/', views.top_global, name='top_global'),
    path('testing/', views.testing, name='testing'),
]