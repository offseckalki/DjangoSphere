from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django import forms



class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']