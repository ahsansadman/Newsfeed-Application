from django.shortcuts import render
from newsapi import NewsApiClient
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Account, Source
from .serializers import *
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login, logout
# Create your views here.

newsapi = NewsApiClient(api_key='f814e1c6740942ca9f5a6dfbfcf31d1b')

# @csrf_exempt
@api_view(['GET', 'POST'])
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response("User is logged in")
        ...
    else:
        return Response("login failed")


@api_view()
def logout_view(request):
    logout(request)
    return Response("User is logged out")


@api_view()
def news(request):
    country = request.GET.get('country')
    source = request.GET.get('source')
    
    if country and source:
       return Response("Select either country or source")
    
    if country:
        top_headlines = newsapi.get_top_headlines(
                                            country=country)
        
    if source:
        top_headlines = newsapi.get_top_headlines(
                                            sources=source)
        
    return Response(top_headlines)
@api_view()
def update_sources(request):
    sources = newsapi.get_sources()['sources']
    
    for source in sources:
        source_data = Source.objects.create(id=source['id'])
        source_data.save()
    
    return Response(sources)
class UserAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
  
    def get(self,request):
        try:
            account = Account.objects.get(user=request.user)
            serializer = AccountSerializer(account)
            return Response(serializer.data)           
        except Account.DoesNotExist:
            return Response('No account found')    
    def patch(self, request):
        try:
            
            account = Account.objects.get(user=request.user)
            serializer = AccountSerializer(account, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Account.DoesNotExist:
            raise Response('Update failed')
    def delete(self, request):
        try:
            
            account = Account.objects.get(user=request.user)
            
            account.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) 
        except Account.DoesNotExist:
            raise 'Deletion failed'          


class UserNewsfeed(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            account = Account.objects.get(user=request.user)
            countries = account.country

            source_list = '' 
            source_set = account.source.all()     
            for source in source_set:
                if not source_list:
                    source_list = source_list + source.id 
                else:
                    source_list = source_list +  ',' +source.id 

            newsfeed = []

            for country in countries:
                # print(country.code)
                news_list =  newsapi.get_top_headlines(
                                        country=str(country.code).lower())
                # print(news_list)           
                for news in news_list['articles']:
                    if news['source']['id'] is None:
                        continue
                    else:
                        item = {
                            'headline' : news['title'],
                            'thumbnail': news['urlToImage'],
                            'source' : news['url'],
                            'country' : country.name,
                        }
                        newsfeed.append(item) 


            return Response(newsfeed)           
        except Account.DoesNotExist:
            return Response('No account found')    