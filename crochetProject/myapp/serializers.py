from rest_framework import serializers
from .models import Pattern, Category, Author

class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = ['title', 'description', 'price', 'difficulty_level', 'author', 'categories']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['user', 'bio']