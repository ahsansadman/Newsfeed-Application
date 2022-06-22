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
   
        
