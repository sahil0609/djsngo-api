from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.urls import reverse




class test_admin(TestCase):

    def setUp(self):
        ''' do the setup before running test'''
        self.client=Client()
        self.superuser=get_user_model().objects.create_superuser(
             email='admin@admin.com',
             password='password'
         )

        self.client.force_login(self.superuser)
      
        self.user=get_user_model().objects.create_user(
            'abc@gmail.com',
            'abcd',
            name='test_user'
        )


    def test_user_listed(self):
        ''' test that user are listed in the admin page '''
        url=reverse('admin:core_customuser_changelist')
        response=self.client.get(url)
        self.assertContains(response,self.user.name)
        self.assertContains(response,self.user.email)
        

    def test_user_change_page(self):
            ''' verify the user change page'''
            url=reverse('admin:core_customuser_change',args=[self.user.id])
            response=self.client.get(url)
            self.assertEqual(response.status_code,200)
            
            
    def test_create_user_page(self):
        '''verify create user page'''
        url=reverse('admin:core_customuser_add')
        response=self.client.get(url)
        self.assertEquals(response.status_code,200)
        
            

    


