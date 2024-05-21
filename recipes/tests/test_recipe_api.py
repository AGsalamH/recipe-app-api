from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from recipes.models import Recipe
from recipes.api.serializers import RecipeSerializer
from tags.models import Tag
from ingredients.models import Ingredient


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
        self.assertFalse(Recipe.objects.filter(
            id=self.recipe.id).exists()
        )

    def test_create_recipe_with_tags(self):
        '''Test Creating a recipe with multiple tags'''
        payload = {
            'title': 'My new recipe',
            'description': 'This is a recipe with multiple tags',
            'price': Decimal('7.00'),
            'time_in_minutes': 15,
            'tags': [
                {'name': 'Fast-Food'},
                {'name': 'meat'},
                {'name': 'Mashroom'},
            ]
        }

        response = self.client.post(get_recipe_urls(), payload, format='json')
        qs = Recipe.objects.filter(
            id=response.data['id']
        ).select_related('user').prefetch_related('tags')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(qs.exists())

        recipe = qs.get()
        self.assertEqual(recipe.tags.count(), 3)

        for tag in payload['tags']:
            tag_exists = recipe.tags.filter(
                name=tag['name'],
                user=self.user
            ).exists()

            self.assertTrue(tag_exists)

    def test_create_recipe_with_existing_tags(self):
        '''Test Creating a recipe with tags that already in the DB.'''
        tag = Tag.objects.create(name='Indian', user=self.user)
        payload = {
            'title': 'Indian recipe',
            'description': 'This is a recipe with already existing tags',
            'price': Decimal('10.00'),
            'time_in_minutes': 5,
            'tags': [
                {'name': 'Indian'},  # already exists
                {'name': 'Break-Fast'}  # new
            ]
        }

        response = self.client.post(get_recipe_urls(), payload, format='json')

        qs = Recipe.objects.filter(
            id=response.data['id'],
            user=self.user
        )
        recipe = qs[0]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(recipe.tags.count(), 2)

        for tag in payload['tags']:
            tag_exists = recipe.tags.filter(
                name=tag['name'],
                user=self.user
            ).exists()

            self.assertTrue(tag_exists)

        indian_tag_count = Tag.objects.filter(
            name=payload['tags'][0]['name']
        ).count()

        self.assertEqual(indian_tag_count, 1)

    def test_update_recipe_tags(self):
        '''Test updating recipe tags API'''
        tag = Tag.objects.create(name='Thai', user=self.user)
        self.recipe.tags.add(tag)

        payload = {
            'title': 'Indian recipe',
            'description': 'This is a recipe',
            'price': Decimal('10.00'),
            'time_in_minutes': 5,
            'tags': [
                {'name': tag.name},  # already exists
                {'name': 'Dinner'},  # new
            ]
        }

        response = self.client.patch(
            get_recipe_urls(self.recipe.id),
            payload,
            format='json'
        )

        self.recipe.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, RecipeSerializer(self.recipe).data)
        self.assertEqual(self.recipe.tags.count(), 2)

    def test_create_recipe_with_ingredients(self):
        '''Test create a recipe with list of ingredients.'''
        payload = {
            'title': 'Indian recipe',
            'description': 'This is a recipe',
            'price': Decimal('10.00'),
            'time_in_minutes': 5,
            'ingredients': [
                {'name': 'ingredient1'},
                {'name': 'ingredient2'},
            ]
        }
        response = self.client.post(get_recipe_urls(), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(
            id=response.data['id'],
            user=self.user
        )

        self.assertEqual(
            recipe.ingredients.count(),
            len(payload['ingredients'])
        )

        for ingredient in payload['ingredients']:
            ingredient_qs = recipe.ingredients.filter(
                name=ingredient['name'],
                user=self.user
            )

            self.assertTrue(ingredient_qs.exists())
            # make sure no duplicates
            self.assertEqual(ingredient_qs.count(), 1)

    def test_create_recipe_with_existing_ingredients(self):
        '''Test creating a recipe with already existing ingredients.'''
        ingredient = Ingredient.objects.create(
            name='ingredient1',
            user=self.user
        )
        payload = {
            'title': 'Indian recipe',
            'description': 'This is a recipe',
            'price': Decimal('10.00'),
            'time_in_minutes': 5,
            'ingredients': [
                {'name': ingredient.name},  # exists!
            ]
        }

        response = self.client.post(get_recipe_urls(), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(
            id=response.data['id'],
            user=self.user
        )

        self.assertEqual(
            recipe.ingredients.count(),
            len(payload['ingredients'])
        )

        for ingredient in payload['ingredients']:
            ingredient_qs = recipe.ingredients.filter(
                name=ingredient['name'],
                user=self.user
            )

            self.assertTrue(ingredient_qs.exists())
            # make sure no duplicates
            self.assertEqual(ingredient_qs.count(), 1)
