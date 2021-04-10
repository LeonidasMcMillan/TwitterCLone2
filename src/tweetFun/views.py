from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.utils.http import is_safe_url
from .models import Tweet
from .forms import TweetForm
from .serializers import tweetSerializer, tweetActionsSerializer, tweetCreateSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication


ALLOWED_HOSTS= settings.ALLOWED_HOSTS


def homePage(request, *args, **kwargs):

    return render(request, "pages/home.html",context ={}, status = 200)

@api_view(['POST'])
#@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweetCreateView(request, *args, **kwargs):
    serializer = tweetCreateSerializer(data = request.POST or None)
    if serializer.is_valid(raise_exception = True):
        serializer.save(user = request.user)
        return Response(serializer.data, status = 201)

    return Response({}, status = 400)
    

@api_view(['GET'])
def tweetListView(request, *args, **kwargs):
    querySet = Tweet.objects.all()
    serializer = tweetSerializer(querySet, many = True)

    return Response(serializer.data) 



@api_view(['GET'])
def tweetDetailView(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id = tweet_id)
    if not qs.exists():
        return Response({}, status = 404)
    obj = qs.first()
    serializer = tweetSerializer(obj)
    return Response(serializer.data, status = 200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweetDeleteView(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id = tweet_id)
    if not qs.exists():
        return Response({}, status = 404)
    qs = qs.filter(user = request.user)
    if not qs.exists():
        return Response({"message": "You do not have authorization to delete this Tweet"}, status = 401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet deleted."}, status = 200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweetActionView(request, *args, **kwargs):
    '''
    id is Required
    Like Unlike and Retweet Actions
    '''
    
    serializer = tweetActionsSerializer(data= request.data)
    if serializer.is_valid(raise_exception = True):
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')
        content = data.get('content')
        qs = Tweet.objects.filter(id = tweet_id)
        
        if not qs.exists():
            return Response({}, status = 404)
        
        qs = qs.filter(user = request.user)
        obj = qs.first()
        serializer = tweetSerializer(obj)
        
        if action == "like":
            obj.likes.add(request.user)
            return Response(serializer.data, status = 200)
        
        elif action == "unlike":
            obj.likes.remove(request.user)
            return Response(serializer.data, status = 200)
        
        elif action == "retweet":
            parentObj = obj
            newTweet = Tweet.objects.create(
                user = request.user, 
                parent = parentObj, 
                content = content, 
            )
            serializer = tweetSerializer(newTweet)
            return Response(serializer.data, status = 201)
            
    return Response({}, status = 200)