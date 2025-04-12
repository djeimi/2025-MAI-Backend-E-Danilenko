from django.test import TestCase, Client
from django.urls import reverse
from ..models import Pattern, Category
from django.contrib.auth.models import User

from django.contrib.auth.models import User

class PatternViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Создаем тестовые данные один раз для всех тестов"""
        print("\nСоздаем начальные тестовые данные...")
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.category = Category.objects.create(name="Test Category")
        cls.pattern = Pattern.objects.create(
            title="Test Pattern",
            description="Description",
            price=10.00,
            difficulty_level="beginner",
            author=cls.author
        )
        cls.pattern.categories.add(cls.category)

    def setUp(self):
        """Выполняется перед каждым тестом"""
        self.client = Client()

    def test_create_pattern(self):
        print("\nЗапуск test_create_pattern")
        data = {
            "title": "New Pattern",
            "description": "New Description",
            "price": 15.00,
            "difficulty_level": "beginner",
            "author": self.user.id,
            "categories": [self.category.id]
        }
        response = self.client.post(
            reverse('create_pattern'), 
            data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Pattern.objects.count(), 2)

    def test_search_patterns(self):
        print("\nЗапуск test_search_patterns")
        response = self.client.get(reverse('search'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Pattern')

    def test_patterns_list(self):
        print("\nЗапуск test_patterns_list")
        response = self.client.get(reverse('patterns_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Pattern', str(response.content))

    def tearDown(self):
        print("\nСостояние после теста:")
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM auth_user")
            print("Users:", cursor.fetchall())
        print(f"Users: {User.objects.count()}")
        print(f"Authors: {User.objects.count()}")
        print(f"Patterns: {Pattern.objects.count()}")