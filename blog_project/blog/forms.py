from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Blog, Message

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'nickname']

class UserEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your message here...'}),
        }
