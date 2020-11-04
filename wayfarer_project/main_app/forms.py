from django import forms
from .models import Profile, TravelPost

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("name", "email", "city", "age","image")
        

class PostForm(forms.ModelForm):
    class Meta:
        model = TravelPost
        fields = ("title", 'body', 'image')
        