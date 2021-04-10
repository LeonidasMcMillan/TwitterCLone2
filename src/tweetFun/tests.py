from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tweet
from rest_framework.test import APIClient

User = get_user_model()

class tweetTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username = 'abc', password = 'somepass')
        User.objects.create_user(username = 'def', password = 'somepass')
        
    def test_user_created(self):
        user = User.object.get(username = 'abc')
        self.assertEqual(user.username, 'abc')
        user = User.object.get(username = 'def')
        self.assertEqual(user.username, 'def')
        
    def test_tweet_created(self):
        obj = Tweet.objects.create(content = 'my tweet', user = self.user)
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.user, self.user)
    
    def get_client(self):
        client = APIClient()
        client.login(username = self.user.username, password = 'somepass')
        return client
        
    def test_api_login(self):
        client = self.get_client()
        response = client.get('/api/tweets/')
        self.assertEqual(response.status_code, 200)
        print response.json()