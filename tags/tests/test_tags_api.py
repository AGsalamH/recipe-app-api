import random
import string

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from tags.models import Tag
from tags.api.serializers import TagSerializer

TAGS_API_URL = reverse('tag-list')


def get_tag_endpoint(tag_id):
    '''Return Tag detail endpoint by id'''
    return reverse('tag-detail', args=[tag_id])


def generate_random_string(length=6):
    '''Create and return random string'''
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))


def create_list_of_tags(num_of_tags, user):
    '''Create and return multiple tags.'''
    tags = []
    for _ in range(num_of_tags):
        tag = Tag.objects.create(
            name=generate_random_string(),
            user=user
        )
        tags.append(tag)
    return tags


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

    def test_auth_is_required(self):
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
        tags = Tag.objects.filter(user=self.user).order_by('-id')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_tag_success(self):
        '''Test updating a tag is successful.'''
        self.tag = Tag.objects.create(
            user=self.user,
            name='Test Tag'
        )
        payload = {
            'name': 'Updated name',
            'user': self.user.id,
        }

        response = self.client.put(get_tag_endpoint(self.tag.id), payload)
        self.tag.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, TagSerializer(self.tag).data)
        self.assertEqual(response.data['name'], str(self.tag))

    def test_deleting_tags(self):
        '''Test deleting tag is successful.'''
        tag = create_list_of_tags(1, self.user)[0]
        response = self.client.delete(get_tag_endpoint(tag.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Tag.objects.filter(id=tag.id).exists()
        )
