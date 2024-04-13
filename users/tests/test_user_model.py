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
