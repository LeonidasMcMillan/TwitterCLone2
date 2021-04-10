from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class tweetLike(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)
    


class Tweet(models.Model):
    
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField(blank = True, null = True)
    image = models.ImageField(upload_to='images/',blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through = tweetLike)
    timestamp = models.DateTimeField(auto_now_add = True)
    parent = models.ForeignKey("self", null = True, on_delete = models.SET_NULL)
    
    
    
    def __str__(self):
        return self.content
    
    class Meta:
        ordering =['-id']
    
    @property
    def isRetweet(self):
        return self.parent != None
    