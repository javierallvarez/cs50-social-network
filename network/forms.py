from django import forms
from django.forms import ModelForm
from .models import *

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'my-form', 
                'id': 'comment-id', 
                'placeholder': "Let your friends know your thoughts", 
                'rows': '6'
            })
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['banner', 'banner_side', 'avatar', 'bio']
        widgets = {
            'banner': forms.URLInput(attrs={
                'class': 'my-form', 
                'id': 'banner-id', 
                'placeholder': "Add a header pic"
            }),
            'banner_side': forms.URLInput(attrs={
                'class': 'my-form', 
                'id': 'banner-id', 
                'placeholder': "Add a lateral pic"
            }),
            'avatar': forms.URLInput(attrs={
                'class': 'my-form', 
                'id': 'avatar-id', 
                'placeholder': "Add photo"
            }),
            'bio': forms.Textarea(attrs={
                'class': 'my-form',
                'id': 'profile-id', 
                'placeholder': "Tell us your story in 60 characters",
                'rows': '6'
            })
        }