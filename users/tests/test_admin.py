'''
Tests for the Django Admin modifications.
'''
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class TestAdminSite(TestCase):
    '''Tests for Django Admin.'''

    def setUp(self):
        '''Create user and client.'''
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            name='harry Potter',
            password='sample123',
        )
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            name='malfoy',
            password='sample123',
        )
        self.client.force_login(self.admin_user)

    def test_users_list(self):
        '''Test that users are listed on page.'''
        response = self.client.get(reverse('admin:users_user_changelist'))
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.name)

    def test_create_user_page(self):
        '''Test create user page'''
        url = reverse('admin:users_user_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
