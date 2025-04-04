from django.urls import path
from .views import (
    search, patterns_list, create_pattern,
    PatternListCreateView, PatternDetailView,
    CategoryListCreateView, CategoryDetailView,
    AuthorListCreateView, AuthorDetailView
)

urlpatterns = [
    path('search/', search, name='search'),
    path('patterns/list/', patterns_list, name='patterns_list'),  # Изменил путь, чтобы избежать конфликта
    path('patterns/create/', create_pattern, name='create_pattern'),
    path('patterns/', PatternListCreateView.as_view(), name='pattern-list-create'),
    path('patterns/<int:pk>/', PatternDetailView.as_view(), name='pattern-detail'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]