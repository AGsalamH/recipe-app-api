'''
Tests for the user token authentcation.
'''
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


CREATE_TOKEN_URL = reverse('obtain-auth-token')


class TestUserTokenAuth(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email': 'test@example.com',
            'password': 'testpassword@123',
            'name': 'Test User',
        }

        self.user = get_user_model().objects.create_user(
            **self.payload
        )

    def test_create_token(self):
        '''Test Creating and Storing a token for a user'''
        response = self.client.post(CREATE_TOKEN_URL, {
            'email': self.payload['email'],
            'password': self.payload['password'],
        })
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())
        token_exists = Token.objects.filter(
            key=response.json().get('token')
        ).exists()
        self.assertTrue(token_exists)
