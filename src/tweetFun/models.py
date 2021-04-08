from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Tweet(models.Model):
    
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='images/',blank=True, null=True)
    
    def __str__(self):
        return self.content
    
    class Meta:
        ordering =['-id']
    
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": 120,
        }