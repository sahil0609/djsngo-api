from rest_framework import viewsets,mixins,authentication,permissions
from recipe.serializers import TagSerializer,IngredientSerializer
from core.models import tags,ingredients


class TagViewSet(viewsets.GenericViewSet,mixins.ListModelMixin):
    serializer_class=TagSerializer
    authentication_classes = (
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )

    queryset=tags.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')



class ingredientsViewSet(viewsets.GenericViewSet,mixins.ListModelMixin):
    serializer_class=IngredientSerializer
    authentication_classes = (
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )

    queryset=ingredients.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')


    
