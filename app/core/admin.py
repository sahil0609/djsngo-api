from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext as _


class userAdmin(BaseUserAdmin):
    ordering=['id']
    list_display=['email','name']
    fieldsets=(
        (None,{"fields":("email","password")}),
         (_("Personal Info"),{"fields":("name",)}),
         (_("Permisssions"),{"fields":("is_active","is_staff","is_superuser")}),
         (_("Important Dates"),{"fields":("last_login",)})
         )
    
    add_fieldsets=(
        (None,{"classes":("wide",),
            "fields":("email","password","password2")}),
        
    )
    
admin.site.register(models.CustomUser,userAdmin)
admin.site.register(models.tags)
admin.site.register(models.ingredients)