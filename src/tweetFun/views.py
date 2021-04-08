from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.utils.http import is_safe_url
from .models import Tweet
from .forms import TweetForm
from .serializers import tweetSerializer
from rest_framework.response import response
from rest_framework.decorators import api_view


ALLOWED_HOSTS= settings.ALLOWED_HOSTS


def homePage(request, *args, **kwargs):

    return render(request, "pages/home.html",context ={}, status = 200)

@api_view(['POST'])
def tweetCreateView_DRF(request, *args, **kwargs):
    serializer = tweetSerializer(data = request.POST or None)
    if serializer.is_valid(raise_exception = True):
        serializer.save(user = request.user)
        return Response(serializer.data, status = 201)

    return Response({}, status = 400)
    

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    querySet = Tweet.objects.all()
    serializer = tweetSerializer(querySet, mnay = True)

    return Response(serializer.data) 



@api_view(['GET'])
def tweetDetailView(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id = tweet_id)
    if not qs.exists():
        return Response({}, status = 404)
    obj = qs.first()
    serializer = tweetSerializer(obj)
    return Response(serializer.data, status = 200)



