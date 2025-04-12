from rest_framework import serializers
from .models import Pattern, Category
from django.contrib.auth.models import User

class PatternSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True,
        queryset=Category.objects.all(),
        slug_field='name'
    )
    
    class Meta:
        model = Pattern
        fields = ['title', 'description', 'price', 'difficulty_level', 'author', 'categories']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']