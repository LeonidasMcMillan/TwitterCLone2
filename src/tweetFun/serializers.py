from rest_framework import serializers
from .models import Tweet
from django.conf import settings

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class tweetCreateSerializer( serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes']
        
    def get_likes(self, obj):
        return obj.likes.count()
        
    def validate_content(self,value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This Tweets is longer than the character limit. Tweets must be "+ str(MAX_TWEET_LENGTH) +" characters or less.")
        return value
class tweetSerializer( serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only = True)
    content = serializers.SerializerMethodField(read_only = True)
    parent = tweetCreateSerializer(read_only = True)
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes', 'isRetweet', 'parent']
        
    def get_likes(self, obj):
        return obj.likes.count()
    
    def get_content(self, obj):
        content = obj.content
        if obj.isRetweet:
            content = obj.parent.content
            
        return content



class tweetActionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank = True, required = False)
    
    def validate_action(self, value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action on a Tweet.")
        return value
    

