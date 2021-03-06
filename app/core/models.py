from django.db import models
from django.contrib.auth.models import  AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra):
        ''' creates the custom user required '''
        if not email:
            raise ValueError('Please provide the email')
        user=self.model(email=self.normalize_email(email),**extra)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password,**extra):
        '''creates a super user'''
        user=self.create_user(email,password,**extra)
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)

        return user



class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    
    objects=UserManager()

    USERNAME_FIELD='email'




class tags(models.Model):
    name=models.CharField(max_length=255)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)    

    
    def __str__(self):
        return self.name


class ingredients(models.Model):
    name=models.CharField(max_length=255)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.name 


class recipe(models.Model):

    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    time_minutes=models.IntegerField()
    price=models.DecimalField(max_digits=5,decimal_places=2)
    link=models.TextField(blank=True)

    tags=models.ManyToManyField('tags')   
    ingredients=models.ManyToManyField('ingredients')

    def __str__(self):
        return self.title 


