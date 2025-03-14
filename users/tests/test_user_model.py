from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserModelTestCase(TestCase):

    def test_create_user_with_email(self):
        '''Test creating user with Email is successfull'''
        name = 'Ahmed Gamal'
        email = 'agsalamh@test.com'
        password = 'testpassword@123456'
        user = User.objects.create_user(
            name=name,
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertNotEqual(user.password, password)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''Test Email is normalized before it's stored for new users'''
        sample_emails = [
            ['test1@example.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['test3@Example.COM', 'test3@example.com'],
            ['test4@EXAMPLE.com', 'test4@example.com'],
        ]

        for email, expected, in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='sample123',
                name='test'
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        '''Test creating users without email raises a ValueError'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                name='ahmed',
                password='sample123',
                email=''
            )

    def test_new_user_with_invalid_email_raises_error(self):
        '''Test creating users with invalid email raises a ValidationError'''
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                name='test',
                password='sample123',
                email='test'
            )

    def test_create_superuser(self):
        '''Test creating superuser'''
        user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            name='admin',
            password='sample123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
