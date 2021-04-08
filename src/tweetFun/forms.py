from django import forms
from .models import Tweet

MAX_TWEET_LENGTH = 140

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
        
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This Tweets is longer than the character limit. Tweets must be "+ str(MAX_TWEET_LENGTH) +" characters or less.")
        return content