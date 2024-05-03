'''
Tests for the user API
'''
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from users.tests.test_token_auth import USER_PROFILE_URL


CREATE_USER_URL = reverse('users:create')


def create_user(**params):
    '''Create and return a new user.'''
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    '''Test the public features of the users API.'''

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email': 'test@exampl.com',
            'password': 'sample@123456789.me',
            'name': 'Test Name'
        }

    def test_create_user_success(self):
        '''Test Creating a user is successful.'''
        response = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=self.payload['email'])
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_with_email_exists_error(self):
        '''Test error returned if user with email already exists.'''
        create_user(**self.payload)
        response = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        '''Test an error is returned if password < 8 characters'''
        response = self.client.post(
            CREATE_USER_URL,
            {**self.payload, 'password': 'abc@123'}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=self.payload['email']
        ).exists()
        self.assertFalse(user_exists)


class PrivateUserAPITests(TestCase):
    '''Test API requests that require authentication'''

    def setUp(self):
        ''' Create and authenticate user.'''
        self.client = APIClient()
        self.payload = {
            'email': 'test@example.com',
            'password': 'pass@123456',
            'name': 'Test User'
        }
        self.user = create_user(**self.payload)
        self.client.force_authenticate(self.user)
        # response = self.client.post(CREATE_TOKEN_URL, self.payload)
        # self.token = response.json().get('token')

    def test_retrieve_profile_success(self):
        '''Test retrieving profile for logged in user.'''
        response = self.client.get(
            reverse(USER_PROFILE_URL, args=(self.user.id,)))
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data, {
                'email': 'test@example.com',
                'name': 'Test User'
            },
        )

    def test_post_profile_not_allowed(self):
        '''Test POST request for profile endpoint NOT ALLOWED.'''
        response = self.client.post(
            reverse(USER_PROFILE_URL, args=(self.user.id,)), {})
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_update_profile_for_authenticated_user(self):
        '''Test Updating profile for a logged in user.'''
        payload = {
            'name': 'updated name',
            'password': 'new password'
        }
        response = self.client.put(
            reverse(USER_PROFILE_URL, args=(self.user.id,)),
            data=payload
        )
        self.user.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
