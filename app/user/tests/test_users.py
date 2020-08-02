from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from  rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL=reverse('user:create')
TOKEN_URL=reverse('user:token')
UPDATE_URL=reverse('user:me')

def create_user(**param):
    return get_user_model().objects.create_user(**param)


class Public_user_api_test(TestCase):
    ''' test public user api's'''
    
    def setUp(self):
        self.client=APIClient()
        
    def test_create_valid_user(self):
        ''' verify the create_user API'''
        payload={
            "email":"abc@gmail.com",
            "name":"abcd",
            "password":"pass123"
        }
        res=self.client.post(CREATE_USER_URL,payload)
        
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user=get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)
        self.assertEqual(payload['email'],user.email)
        
    def test_user_exists(self):
        ''' check create_user if user already exists'''
        payload={
        "email":"abc@gmai.com",
        "password":"abcde",  
        "name":"test1"  
        } 
        create_user(**payload)
        res=self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_password(self):
        """ verify if password matches requirements"""
        payload={
            "email":"abc@gmail.com",
            "password":"a",
            "name":"test1"
        }
        res=self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user=get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user)
        
    
    def test_generate_token_api(self):
        """ verify the token for an valid user"""
        
        payload = {
            "email":"test@gmail.com",
            "password":"test123"
        }

        create_user(**payload)
        res=self.client.post(TOKEN_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertIn('token',res.data)

    def test_generate_token_not_existing_user(self):
        """ try to generate a token for a non existing user """
        payload = {
            "email":"test@gmail.com",
            "password":"test123"
        }

        res=self.client.post(TOKEN_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


    def test_generate_token_invalid_password(self):
        """ try to generate a token by giving a inavlid password """
        
        payload = {
            "email":"test@gmail.com",
            "password":"test123"
        }
        create_user(**payload)
        payload['password']="abc@123"
        res=self.client.post(TOKEN_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


    def test_generate_token_empty_password(self):
        """ try to generate a token for giving a empty password """
        payload = {
            "email":"test@gmail.com",
            "password":"test123"
        }
        create_user(**payload)
        payload.pop("password",None)
        res=self.client.post(TOKEN_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    
    def test_change_user_unauthorized(self):
        """ verify the update user API for unauthenticated user """
        
        res=self.client.get(UPDATE_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)



    class private_user_tests(TestCase):
        """ test for testing the private APi"""

        def setUp(self):
            self.user=create_user(
                email="abcd@gmail.com",
                password="abcde",
                name="test"
            )
            self.client=APIClient()
            self.client.force_authenticate(user=self.user)

        def test_update_user_API(self):
            """ test the update API """
            res=self.client.get(UPDATE_URL)
            self.assertEqual(res.status_code,status.HTTP_200_OK)
            self.assertEqual(res.data,{"email":self.user.email,"name":self.user.name})


        def test_update_successful(self):
            """ test the user is updated """
            payload = {
                "name":"new user",
                "password":"test123"
            }

            res=self.client.patch(UPDATE_URL,payload)
            self.assertEqual(res.status_code,status.HTTP_200_OK)
            self.user.refersh_from_db()
            self.assertEqual(self.user.email,payload['email'])
            self.assertTrue(self.user.check_password(payload['password']))


        
        