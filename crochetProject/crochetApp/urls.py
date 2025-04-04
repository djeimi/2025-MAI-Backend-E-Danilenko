from django.urls import path
from .views import search, patterns_list, create_pattern

urlpatterns = [
    path('search/', search, name='search'),
    path('patterns/', patterns_list, name='patterns_list'),
    path('patterns/create/', create_pattern, name='create_pattern'),
]