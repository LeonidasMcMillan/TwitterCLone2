from django.contrib import admin
from django.urls import path

from .views import (
    tweetCreateView, 
    homePage, 
    tweetDetailView, 
    tweetListView, 
    tweetDeleteView,
    tweetActionView
    )

urlpatterns = [
    path('<int:tweet_id>/', tweetDetailView),
    path('', tweetListView),
    path('create-tweet/', tweetCreateView),
    path('<int:tweet_id>/delete/', tweetDeleteView),
    path('action/', tweetActionView),
    
]
