from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from  rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL=reverse('user:create')

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
        user=get_user_model.objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)
        self.assertEqual(payload['email'],user.email)
        
    def test_user_exists(self):
        ''' check create_user if user already exists'''
        payload={
        "email":"abc@gmai.com",
        "password":"abcde"    
        } 
        create_user(**payload)
        res=self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_password(self):
        """ verify if password matches requirements"""
        payload={
            "email":"abc@gmail.com",
            "password":"a",
        }
        res=self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user=get_user_model.objects.filter(email=payload['email']).exists()
        self.assertFalse(user)
        
    
        
        