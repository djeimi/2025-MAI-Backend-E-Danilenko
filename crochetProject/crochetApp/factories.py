import factory
from .models import Pattern, Category

import factory
from django.contrib.auth.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'testuser{n}')
    email = factory.Sequence(lambda n: f'testuser{n}@example.com')

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "Test Category"

class PatternFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pattern

    title = "Test Pattern"
    description = "Description"
    price = 10.00
    difficulty_level = "beginner"
    author = factory.SubFactory(UserFactory)  # Будет создавать нового автора с новым пользователем

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)
        else:
            # Добавляем категорию по умолчанию, если не указаны
            self.categories.add(CategoryFactory())
