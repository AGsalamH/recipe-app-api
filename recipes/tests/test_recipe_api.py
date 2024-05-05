from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from recipes.models import Recipe


def get_recipe_urls(arg=None):
    'Construct and return DETAIL or LIST API URL.'
    if arg:
        return reverse('recipe-detail', args=[arg])
    return reverse('recipe-list')


class TestRecipeAPI(TestCase):
    '''Test Recipe API endpoints.'''
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='test@pass',
            name='Test User'
        )
        self.payload = {
            'title': 'My First Recipe',
            'description': 'This is my first recipe.',
            'time_in_minutes': 4,
            'price': Decimal('6.50'),
            'user': self.user
        }

        self.recipe = Recipe.objects.create(**self.payload)
        self.client.force_authenticate(self.user)

    def test_auth_required(self):
        '''Test auth is required to call API.'''
        self.client.logout()
        response = self.client.get(get_recipe_urls())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_recipes(self):
        '''Test LIST recipes API endpoint.'''
        response = self.client.get(get_recipe_urls())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_recipe_success(self):
        '''Test CREATE recipe API endpoint.'''
        response = self.client.post(
            get_recipe_urls(),
            {**self.payload, 'user': self.user.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_recipe_success(self):
        '''Test UPDATE recipe API endpoint.'''
        updated_values = {
            'title': 'Test Title',
            'price': Decimal('7.00'),
            'link': f'http://test.com/recipes/{self.recipe.id}'
        }
        response = self.client.patch(
            get_recipe_urls(self.recipe.id),
            updated_values
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe.refresh_from_db()
        self.assertEqual(str(self.recipe), updated_values['title'])
        self.assertEqual(self.recipe.price, updated_values['price'])
        self.assertEqual(self.recipe.link, updated_values['link'])

    def test_delete_recipe(self):
        '''Test Deleting a recipe.'''
        response = self.client.delete(get_recipe_urls(self.recipe.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
