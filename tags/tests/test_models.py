'''
Test Tag related models.
'''

from django.test import TestCase
from django.contrib.auth import get_user_model
from tags.models import Tag


class TestTagModel(TestCase):
    '''Tag model Tests.'''

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='test@password',
            name='Test User'
        )

    def test_Create_tag(self):
        '''Test Creating a tag is successful.'''
        tag_payload = {
            'name': 'Test Tag',
            'user': self.user
        }

        tag = Tag.objects.create(**tag_payload)

        self.assertEqual(str(tag), tag_payload['name'])
        self.assertEqual(tag.user, tag_payload['user'])
