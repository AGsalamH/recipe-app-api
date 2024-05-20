from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from ingredients.models import Ingredient


class TestIngredientModel(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name='Test User',
            email='test@example.com',
            password='test@password'
        )
        self.client.force_authenticate(self.user)

    def test_create_ingredient(self):
        '''Test creating ingredient successfully.'''
        ingredient = Ingredient.objects.create(
            name='ingredient1',
            user=self.user
        )

        self.assertEqual(str(ingredient), ingredient.name)
