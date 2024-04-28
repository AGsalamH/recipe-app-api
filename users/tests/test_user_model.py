from django.test import TestCase
from django.contrib.auth import get_user_model

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
