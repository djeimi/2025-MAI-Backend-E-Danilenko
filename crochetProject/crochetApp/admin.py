from django.contrib import admin
from .models import Category, Pattern, Review

admin.site.register(Category)
admin.site.register(Pattern)
admin.site.register(Review)