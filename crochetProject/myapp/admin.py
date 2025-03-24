from django.contrib import admin
from .models import Author, Category, Pattern, Review

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Pattern)
admin.site.register(Review)