from django.contrib import admin
from .models import Tweet


class tweetAdmin(admin.ModelAdmin):
    
    list_display = ['__str__', 'user']
    search_fields = ['user__username', 'user__email']
    
    
    class Meta:
        model = Tweet

# Register your models here.
admin.site.register(Tweet,  tweetAdmin)


