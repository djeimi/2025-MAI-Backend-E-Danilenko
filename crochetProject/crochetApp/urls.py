from django.urls import path
from .views import (
    search, patterns_list, create_pattern,
    PatternListCreateView, PatternDetailView,
    CategoryListCreateView, CategoryDetailView,
    UserDetailView, UserListCreateView,
    home, zone51, anon)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('api/search/', search, name='search'),
    path('api/patterns/list/', patterns_list, name='patterns_list'), 
    path('api/patterns/create/', create_pattern, name='create_pattern'),
    path('api/patterns/', PatternListCreateView.as_view(), name='pattern-list-create'),
    path('api/patterns/<int:pk>/', PatternDetailView.as_view(), name='pattern-detail'),
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('api/categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('', home, name='home'),
    path('zone51/', zone51, name='zone51'),
    path('anon/', anon, name='anon'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
]