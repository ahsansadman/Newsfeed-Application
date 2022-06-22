from django.shortcuts import render

from newsapi import NewsApiClient
from rest_framework.decorators import api_view
from rest_framework.response import Response
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