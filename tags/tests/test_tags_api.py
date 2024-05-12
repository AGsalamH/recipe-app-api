import random
import string

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from tags.models import Tag

TAGS_API_URL = reverse('tag-list')


def generate_random_string(length=6):
    '''Create and return random string'''
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))


def create_list_of_tags(num_of_tags, user):
    '''Create and return multiple tags.'''
    for _ in range(num_of_tags):
        Tag.objects.create(
            name=generate_random_string(),
            user=user
        )


class TestTagAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'Test User',
            'test@example.com',
            'test@pass'
        )
        create_list_of_tags(5, self.user)
        self.client.force_authenticate(self.user)

    def test_aut_is_required(self):
        '''Test authentication is required to list tags.'''
        self.client.logout()
        response = self.client.get(TAGS_API_URL)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_list_tags(self):
        '''Test Listing tags is successful.'''
        response = self.client.get(TAGS_API_URL)
        tags = Tag.objects.filter(user=self.user)
        self.assertEqual(response.data, list(tags))
