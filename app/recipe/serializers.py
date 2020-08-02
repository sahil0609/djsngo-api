from rest_framework import serializers
from core.models import tags,ingredients



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