from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from core.models import tags,ingredients,recipe
from recipe.serializers import recipe_serializer,recipe_detail_serializer


RECIPE_URL=reverse('recipe:recipe-list')


def sample_recipe(user,**payload):
    ''' create and returns a sample recipe '''
    default={
        "title":"sample_recipe",
        "price":99.00,
        "time_minutes":5,
    }    
    default.update(payload)

    return recipe.objects.create(user=user,**default)

def sample_tag(user,name="sample_tag"):
    return tags.objects.create(user=user,name=name)

def sample_ingredient(user,name="sample_ingredient"):
    return ingredients.objects.create(user=user,name=name)


def reverse_url(recipe_id):
    return reverse('recipe:recipe-detail',args=[recipe_id])





class publicTest(TestCase):
    """ test recipe endpoints for unauthenticated users """

    def setUp(self):
        self.client=APIClient()


    def test_unauthorized_users(self):
        """ test recipe endpoint for unauthenticated users """
        res=self.client.get(RECIPE_URL)
        
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class privateRecipeAPItests(TestCase):
    """ create test for authorized users """

    def setUp(self):
        self.client= APIClient()

        self.user=get_user_model().objects.create(
            email="test@gmail.com",
            name="abcd",
            password="1234567"
        )

        self.client.force_authenticate(self.user)



    def test_recipe_retrieve(self):

        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res=self.client.get(RECIPE_URL)
        recipe_data=recipe.objects.all().order_by('-id')
        recipe_data=recipe_serializer(recipe_data,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(recipe_data.data,res.data)


    def test_recipe_only_for_user(self):
        """ verify recipe cretaed are only for returned for the created user """
        user=get_user_model().objects.create(
            email="aef@gmail.com",
            password="abcdef"
        )

        sample_recipe(user=user)
        sample_recipe(user=self.user,title="abcde")

        res=self.client.get(RECIPE_URL)
        recipe_data=recipe.objects.all().filter(user=self.user)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        recipe_data=recipe_serializer(recipe_data,many=True)
        self.assertEqual(res.data,recipe_data.data)


    def test_recipe_detail(self):
        """ test the detail recipe endpoint """
        recipe=sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        URL=reverse_url(recipe.id)
        res=self.client.get(URL)
        recipe_data=recipe_detail_serializer(recipe)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(recipe_data.data,res.data)


    def test_create_basic_recipe(self):
        """ add the new basic recipe """
        payload={
            "title":"sample",
            "price":99.00,
            "time_minutes":5     
        }

        res=self.client.post(RECIPE_URL,payload)

        

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

        recipe_data=recipe.objects.get(id=res.data["id"])

        for key in payload:
            self.assertEqual(payload[key],getattr(recipe_data,key))


    def test_create_recipe_tags(self):
        """ test a recipe with tags """
        tag1=sample_tag(user=self.user,name="abcd")
        tag2=sample_tag(user=self.user,name="wsad")

        payload={
         "title":"sample_recipe",
         "price":99.00,
         "time_minutes":5,
         "tags":[tag1.id,tag2.id]
        }

        res=self.client.post(RECIPE_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

        recipe_data=recipe.objects.get(id=res.data["id"])
        tags=recipe_data.tags.all()
        
        self.assertIn(tag1,tags)
        self.assertIn(tag2,tags)



    def test_create_recipe_ingredients(self):
        """ test a recipe with ingredients"""
        ingredient1=sample_ingredient(user=self.user,name="abcd")
        ingredient2=sample_ingredient(user=self.user,name="wsad")

        payload={
         "title":"sample_recipe",
         "price":99.00,
         "time_minutes":5,
         "ingredients":[ingredient1.id,ingredient2.id]
        }

        res=self.client.post(RECIPE_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

        recipe_data=recipe.objects.get(id=res.data["id"])
        ingredients=recipe_data.ingredients.all()
        
        self.assertIn(ingredient1,ingredients)
        self.assertIn(ingredient2,ingredients)


    def test_update_recipe(self):
        """ test partial update recipe """

        recipe=sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        new_tag=sample_tag(user=self.user,name="new_tags")

        payload={
         "title":"chicken",
         "tags":[new_tag.id]

        }

        URL=reverse_url(recipe.id)
        res=self.client.patch(URL,payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title,payload['title'])
        tags=recipe.tags.all()
        self.assertEqual(len(tags),1)


    def test_full_update_recipe(self):
        """ test updating recipe with put """

        recipe=sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))

        payload={
            "title":"new recipe",
            "price":99.00,
            "time_minutes":200
        }

        URL=reverse_url(recipe.id)
        res=self.client.put(URL,payload)
        recipe.refresh_from_db()

        self.assertEqual(recipe.title,payload['title'])
        self.assertEqual(recipe.price,payload['price'])
        self.assertEqual(recipe.time_minutes,payload['time_minutes'])

        tags=recipe.tags.all()
        self.assertEqual(len(tags),0)