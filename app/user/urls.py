from django.urls import path
from user.views import user_add_view,get_token_view,update_user_view

app_name="user"

urlpatterns = [
    path('create/',user_add_view.as_view(),name="create"),
    path('token/',get_token_view.as_view(), name='token'),
    path('me/',update_user_view.as_view(), name='me')
]