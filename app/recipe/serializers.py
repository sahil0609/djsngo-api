from rest_framework import serializers
from core.models import tags,ingredients,recipe



class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model=tags
        fields=('id','name')
        read_only_fields = ('id',)

    
class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model=ingredients
        fields=('id','name')
        read_only_fields = ('id',)


class recipe_serializer(serializers.ModelSerializer):

        ingredients=serializers.PrimaryKeyRelatedField(many=True,queryset=ingredients.objects.all())
        tags=serializers.PrimaryKeyRelatedField(many=True,queryset=tags.objects.all())

        class Meta:
            model = recipe
            fields = ('id','title','ingredients','tags','price','time_minutes','link')
            read_only_fields = ('id',)



class recipe_detail_serializer(recipe_serializer):
    """ serialize a recipe detial class """
    ingredients=IngredientSerializer(many=True,read_only=True)
    tags=TagSerializer(many=True,read_only=True)
