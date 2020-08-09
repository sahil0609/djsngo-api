from rest_framework import viewsets,mixins,authentication,permissions
from recipe.serializers import TagSerializer,IngredientSerializer,recipe_serializer,recipe_detail_serializer
from core.models import tags,ingredients,recipe


class TagViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin):
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
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)



class ingredientsViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin):
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


    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


class recipeViewSet(viewsets.ModelViewSet):
    """ vieset  for the recipe endpoint """

    serializer_class=recipe_serializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset=recipe.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

 
    def get_serializer_class(self):
        """ return custom serializer class based on action """

        if self.action=='retrieve':
            return recipe_detail_serializer

        return self.serializer_class


    def perform_create(self,serializer):
        """ create a new recipe """
        serializer.save(user=self.request.user)



