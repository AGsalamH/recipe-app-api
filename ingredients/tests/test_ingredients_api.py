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

    def test_auth_required(self):
        '''Test that authentication is required to access API.'''
        self.client.logout()
        response = self.client.get(INGREDIENTS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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

    def test_create_ingredient(self):
        '''Test creating ingredient endpoint.'''
        payload = {'name': 'ingredient1'}
        response = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], payload['name'])

        ingredient = Ingredient.objects.get(user=self.user)
        self.assertEqual(response.data, IngredientSerializer(ingredient).data)

    def test_retrieve_ingredient(self):
        '''Test retrieving single ingredient by ID.'''
        ingredient = Ingredient.objects.create(
            name='test ingredient',
            user=self.user
        )

        response = self.client.get(retrieve_url(ingredient.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, IngredientSerializer(ingredient).data)

    def test_retrieve_not_existed_ingredient(self):
        '''Test retrieving ingredient that does NOT exist!'''
        dummy_id = 123
        response = self.client.get(retrieve_url(dummy_id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_ingredient(self):
        '''Test deleting ingredient is successful.'''

        ingredient = Ingredient.objects.create(
            name='test ingredient',
            user=self.user
        )
        response = self.client.delete(retrieve_url(ingredient.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Ingredient.objects.filter(user=self.user).exists()
        )

    def test_delete_ingredient_not_found(self):
        '''Test deleting ingredient faliure.'''

        dummy_id = 123
        response = self.client.delete(retrieve_url(dummy_id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
