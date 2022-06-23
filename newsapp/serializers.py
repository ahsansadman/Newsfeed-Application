from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate

class SourcesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Source 
        fields = ('__all__')


class AccountSerializer(CountryFieldMixin,WritableNestedModelSerializer):
    
    source = SourcesSerializer(many=True)
    tag = TagListSerializerField()
    class Meta:
        model = Account 
        fields = ('user','country','source','tag',)
   
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')
    
class ChangePasswordSerializer(serializers.Serializer):
    
    model = User


    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)