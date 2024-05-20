from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser

from rest_framework import status
from rest_framework.test import APIClient

from core.utils import generate_random_string

from ingredients.models import Ingredient
from ingredients.api.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('ingredient-list')


def retrieve_url(id):
    '''Get ingredient detail URL eg: /ingredients/<id>'''
    return reverse('ingredient-detail', args=(id,))


def create_ingredients(user: AbstractBaseUser, num: int = 1):
    '''Create and return number of ingredients.'''
    ingredients: list[Ingredient] = []
    for _ in range(num):
        ingredients.append(Ingredient(
            name=generate_random_string(),
            user=user
        ))
    return Ingredient.objects.bulk_create(ingredients)


class TestIngredientsAPI(TestCase):
    '''Testing Ingredients API endpoints.'''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name='Test User',
            email='test@example.com',
            password='test@password'
        )
        self.client.force_authenticate(self.user)

    def test_list_ingredients(self):
        '''Test List ingredients endpoint.'''
        num_of_ingredients = 3
        create_ingredients(self.user, num_of_ingredients)
        response = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.filter(
            user=self.user
        ).order_by('-name')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), num_of_ingredients)
        self.assertEqual(
            response.data,
            IngredientSerializer(ingredients, many=True).data
        )
