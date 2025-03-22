from django.urls import path
from .views import profile, product_list, category_page

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('products/', product_list, name='product_list'),
    path('category/', category_page, name='category_page'),
]