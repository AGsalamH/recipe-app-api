'''
Tests for the Recipe model.
'''
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from recipes.models import Recipe


class TestRecipeModel(TestCase):
    '''Recipe model test cases.'''

    def test_create_recipe_successful(self):
        user = get_user_model().objects.create_user(
            email='test@example.com',
            name='Test User',
            password='test@password'
        )

        recipe = Recipe.objects.create(
            user=user,
            title='My first Recipe',
            time_in_minutes=5,
            price=Decimal('6.50')
            description='This is my first recipe.'
        )
        self.assertEqual(str(recipe), recipe.title)
