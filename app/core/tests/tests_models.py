from  django.test import TestCase
from  django.contrib.auth import get_user_model


class Modeltests(TestCase):


    def test_create_user(self):
        ''' create a test user '''
        email='abc@email.com'
        password='password'
        user=get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_email_normalize(self):
        ''' checks the normalized email for the new user'''
        email='ABC@EMAIL.COM'
        password='password'
        user=get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email,'ABC@email.com')

    def test_validate_email(self):
        ''' if email is None raise a error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None,password='password')


    def test_create_super_user(self):
        ''' validting crating new super user'''
        user=get_user_model().objects.create_superuser(
            email='admin@admin.com',
            password='password'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

