from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from recipe.serializers import TagSerializer,IngredientSerializer

from core.models import tags,ingredients


TAGS_URL=reverse('recipe:tags-list')
INGREDIENTS_URL=reverse('recipe:ingredients-list')

class PublicAPITest(TestCase):
    ''' to test recipe API for unauthorized users '''

    def setUp(self):
        self.user=get_user_model().objects.create(
            email="email@gmail.com",
            name="abcd@gmail.com",
            password="abcde"
        )

    def test_get_tag_unauthorized(self):
            ''' tes the tags endpoint without authorizations'''
            res=self.client.get(TAGS_URL)
            self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


    def test_get_ingredients_unauthorized(self):
            ''' test the ingredients endpoint without authorization'''
            res=self.client.get(INGREDIENTS_URL)
            self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)  
    

    
class PrivatAPITest(TestCase):
    ''' to test recipe api for authorized users '''
    
    def setUp(self):
        self.user=get_user_model().objects.create(
            email='abcd@gmail.com',
            password='password',
            name='name'
        )
        self.client=APIClient()
        self.client.force_authenticate(user=self.user)


    def test_get_tags(self):
        ''' test the api returns tags '''
        tags.objects.create(user=self.user,name="vegan")
        
        tags_obj=tags.objects.all().order_by('-name')
        res=self.client.get(TAGS_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        data=TagSerializer(tags_obj,many=True)
        self.assertEqual(res.data,data.data)


    def test_user_specified_tags(self):
        ''' test the API returns only user created tags '''
        user_temp=get_user_model().objects.create(
            email="abcd!gmail.com",
            password="abcdef"
        )

        tags.objects.create(user=user_temp,name='not my tag')
        tags.objects.create(user=self.user,name='my tag')

        res=self.client.get(TAGS_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],'my tag')


    def test_ingredients_tags(self):
        ''' test the ingredients endpoint '''
        ingredients.objects.create(user=self.user,name="banana")

        res=self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        ingredients_obj=ingredients.objects.all().order_by('-name')
        data=IngredientSerializer(ingredients_obj, many=True)
        self.assertEqual(data.data,res.data)


    def test_user_specified_ingredients(self):
        ''' test that API only returns user made ingredients '''

        user_temp=get_user_model().objects.create(
            email="abcd!gmail.com",
            password="abcdef"
        )

        ingredients.objects.create(user=user_temp,name='not my ingredient')
        ingredients.objects.create(user=self.user,name='my ingredient')

        res=self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],'my ingredient')

        




    