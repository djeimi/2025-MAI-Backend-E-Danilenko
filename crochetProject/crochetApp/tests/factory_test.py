from django.test import TestCase
from crochetApp.models import Pattern
from crochetApp.factories import CategoryFactory, PatternFactory

class PatternModelTests(TestCase):
    def test_create_pattern(self):
        # Создаем паттерн с автоматически созданными автором и пользователем
        pattern = PatternFactory()
        self.assertEqual(Pattern.objects.count(), 1)
        
        # Или с конкретной категорией
        category = CategoryFactory(name="Specific Category")
        pattern_with_category = PatternFactory(categories=[category])
        self.assertEqual(pattern_with_category.categories.count(), 1)