from django.shortcuts import render
from newsapi import NewsApiClient
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Account, Source
from .serializers import *
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

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
