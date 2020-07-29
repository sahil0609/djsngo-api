from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models


class userAdmin(BaseUserAdmin):
    ordering=['id']
    list_display=['email','name']
    
    
admin.site.register(models.CustomUser,userAdmin)