from rest_framework import generics,authentication,permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import user_serializers,token_serializer

class user_add_view(generics.CreateAPIView):
    """ add a new user """
    serializer_class = user_serializers 


class get_token_view(ObtainAuthToken):
    """ get a new TOKEN  for a user """
    serializer_class=token_serializer
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES

class update_user_view(generics.RetrieveUpdateAPIView):

    serializer_class=user_serializers
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user