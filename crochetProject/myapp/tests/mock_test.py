from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse

from django.test import TestCase, Client
from django.urls import reverse
from ..models import Pattern, Author, Category
from django.contrib.auth.models import User

class MockTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Создаем тестовые данные один раз для всех тестов"""
        print("\nСоздаем начальные тестовые данные...")
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.author = Author.objects.create(
            user=cls.user,  
            bio="Author bio"
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

    @patch('myapp.views.Pattern.objects.filter')
    def test_search_with_mock(self, mock_filter):
        mock_filter.return_value = []
        response = self.client.get(reverse('search'), {'q': 'Test Pattern'})
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
