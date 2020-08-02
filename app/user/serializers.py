from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from django.utils.translation import ugettext_lazy as _ 

class user_serializers(serializers.ModelSerializer):
    """ serialize the user model """
    
    class Meta:
        model=get_user_model()
        fields = ('email','password','name')
        extra_kwargs = {'password':{'write_only':True,"min_length":5}}
    

    def create(self,validated_data):
        """create a new user using validate_data"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self,instance,validated_data):
        """ update a user model """
        password=validated_data.pop('password',None)
        user=super.update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        

class token_serializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':"password"},
        trim_whitespace=False
    )


    def validate(self,attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        user=authenticate(
            request=self.context.get('request'),
            email=email,password=password)

        if not user:
            msg=_('no user is found with these crendtials')
            raise serializers.ValidationError(msg,code='authorization')
        attrs['user']=user
        return attrs
            


        











