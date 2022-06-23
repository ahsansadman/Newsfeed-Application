from django.shortcuts import render
from newsapi import NewsApiClient
from requests.models import StreamConsumedError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Account, Source
from .serializers import *
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
import json
from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule

import sendgrid
from sendgrid import SendGridAPIClient
import os
from sendgrid.helpers.mail import *

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

# Create your views here.

newsapi = NewsApiClient(api_key='f814e1c6740942ca9f5a6dfbfcf31d1b')

    
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

@shared_task
def get_newsfeed(account):
    
    countries = account.country
    
    source_list = '' 
    source_set = account.source.all()     
    for source in source_set:
        if not source_list:
            source_list = source_list + source.id 
        else:
            source_list = source_list +  ',' +source.id 
            
    newsfeed = []
    keyword = list(account.tag.names())
    tag_apear = False
    # print(keyword)
    for country in countries:
        # print(country.code)
        news_list =  newsapi.get_top_headlines(
                                country=str(country.code).lower())
                
        for news in news_list['articles']:
            if news['source']['id'] is None:
                continue
            elif news['source']['id'] in source_list:
                item = {
                    'headline' : news['title'],
                    'thumbnail': news['urlToImage'],
                    'source' : news['url'],
                    'country' : country.name,
                }
                newsfeed.append(item)
                for key in keyword:
                    if key in news['title']:
                        sendemail(account,news['title'],key)          
   
    try:
        feed_info = Newsfeed.objects.get(user=account.user)
        feed_info.newsfeed = json.dumps(newsfeed)
        feed_info.save()
    except Newsfeed.DoesNotExist:
        feed_info = Newsfeed.objects.create(user = account.user,newsfeed=json.dumps(newsfeed))
        feed_info.save()
        add_interval_task(account)   
    return newsfeed


def add_interval_task(account):

    schedule, created = IntervalSchedule.objects.get_or_create(
     every=10,
     period=IntervalSchedule.MINUTES,)

    PeriodicTask.objects.create(
         interval=schedule,                  
         name='Update newsfeed for ' + account.user.username,         
         task='newsapp.views.get_newsfeed',  
         args= (account),
         )
    
    return Response("Task added")


def sendemail(account,content,keyword):
    
    message = Mail(
        from_email='ahsan.sadman@ferntechsolutions.com',
        to_emails=account.user.email,
        subject= str(keyword) +' keyword appeared in your personalized news feed',
        html_content='<strong>'+ content +'</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })    

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class UserAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
  
    def get(self,request):
        try:
            account = Account.objects.get(user=request.user)
            serializer = AccountSerializer(account)
            # sendemail(account,'hello', 'say')
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        try:
            newsfeed_data = Newsfeed.objects.get(user=request.user)
            return Response(json.loads(newsfeed_data.newsfeed)) 
                  
        except Newsfeed.DoesNotExist:
            account = Account.objects.get(user=request.user)
            newsfeed = get_newsfeed(account)
            return Response(newsfeed)         


class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)