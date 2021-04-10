from django.contrib import admin
from .models import Tweet, tweetLike

class tweetLikeAdmin(admin.TabularInline):
    model = tweetLike
class tweetAdmin(admin.ModelAdmin):
    inlines = [tweetLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['user__username', 'user__email']
    class Meta:
        model = Tweet

# Register your models here.
admin.site.register(Tweet,  tweetAdmin)


